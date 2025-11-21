import json
import qrcode
import base64
from io import BytesIO
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    qr_code_image = fields.Binary(
        string='QR Code',
        compute='_compute_qr_code_image',
        store=False,
        help="QR code containing delivery and customer information in CSV format"
    )

    @api.depends('partner_id', 'origin', 'name', 'scheduled_date')
    def _compute_qr_code_image(self):
        """Generate QR code containing sales data in CSV format"""
        for picking in self:
            if picking.picking_type_code == 'outgoing' and picking.partner_id:
                try:
                    # Prepare QR code data
                    qr_data = picking._prepare_qr_data()
                    
                    if qr_data:
                        # Generate QR code
                        qr_code_image = picking._generate_qr_code(qr_data)
                        picking.qr_code_image = qr_code_image
                        _logger.info(f"QR code generated successfully for picking {picking.name}")
                    else:
                        picking.qr_code_image = False
                        _logger.warning(f"No QR data prepared for picking {picking.name}")
                except Exception as e:
                    _logger.error(f"Error generating QR code for picking {picking.name}: {str(e)}")
                    picking.qr_code_image = False
            else:
                picking.qr_code_image = False

    def _prepare_qr_data(self):
        """Prepare data dictionary for QR code"""
        self.ensure_one()
        
        partner = self.partner_id
        if not partner:
            _logger.warning(f"No partner found for picking {self.name}")
            return False

        # Prepare customer address/location
        address_parts = []
        if partner.street:
            address_parts.append(partner.street)
        if partner.street2:
            address_parts.append(partner.street2)
        if partner.city_id:
            address_parts.append(partner.city_id.name)
        if partner.state_id:
            address_parts.append(partner.state_id.name)
        if partner.country_id:
            address_parts.append(partner.country_id.name)
        
        customer_address = ', '.join(address_parts) if address_parts else 'N/A'

        # Prepare QR data dictionary - FIXED: Safe carrier_id access
        qr_data = {
            'order_number': self.origin or self.name,
            'customer_name': partner.name or 'N/A',
            'customer_address': customer_address,
            'customer_phone': partner.phone or partner.mobile or 'N/A',
            'customer_email': partner.email or 'N/A',
            'delivery_method': self.carrier_id.name if self.carrier_id else 'N/A',  # FIXED
            'delivery_order': self.name,
            'delivery_date': str(self.scheduled_date.date()) if self.scheduled_date else 'N/A'
        }

        _logger.info(f"QR data prepared for picking {self.name}: {qr_data}")
        return qr_data

    def _generate_qr_code(self, data):
        """Generate QR code image from data dictionary"""
        try:
            # Convert data to CSV format
            csv_text = self._format_qr_text(data)
            _logger.info(f"CSV text for QR: {csv_text[:100]}...")  # Log first 100 chars
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(csv_text)
            qr.make(fit=True)

            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Ensure clean base64 string (remove any whitespace/newlines)
            qr_code_base64 = qr_code_base64.replace('\n', '').replace('\r', '').strip()
            
            _logger.info(f"QR code base64 generated, length: {len(qr_code_base64)}")
            return qr_code_base64
            
        except Exception as e:
            _logger.error(f"Error generating QR code: {str(e)}")
            return False

    def _format_qr_text(self, data):
        """Format data dictionary into CSV format for QR code"""
        # CSV Header - all field names in one row
        csv_header = "Order Number,Customer Name,Customer Address,Customer Phone,Customer Email,Delivery Method,Delivery Order,Delivery Date"
        
        # CSV Data - all values in one row - IMPROVED: Better None handling
        csv_data = f'"{data.get("order_number", "N/A")}","{data.get("customer_name", "N/A")}","{data.get("customer_address", "N/A")}","{data.get("customer_phone", "N/A")}","{data.get("customer_email", "N/A")}","{data.get("delivery_method", "N/A")}","{data.get("delivery_order", "N/A")}","{data.get("delivery_date", "N/A")}"'
        
        # Combine header and data rows
        csv_content = [csv_header, csv_data]
        
        return '\n'.join(csv_content)