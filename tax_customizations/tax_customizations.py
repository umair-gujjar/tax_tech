from datetime import date
from openerp import models, fields, api
class tax_customizations(models.Model):
    _inherit = "account.tax"
    
    sale_type = fields.Selection([('1', 'Goods at standard rate'),  ('2', 'Third Schedule Goods'), ('3', 'Good at Reduced Rate'), ('4', 'Electricity Supply to Retailers'), ('5', 'Electricity to stell sector'), ('6', 'Gas to CNG stations'), ('7', 'Re-rollable scrap by ship-breakers'), ('8', 'SIM sale / IMEI activation'), ('9', 'Goods (FED in ST Mode)'), ('10', 'Goods at zero-rate'), ('11', 'Exempt goods'), ('12', 'Other'), ('13', 'DTRE goods'), ('14', 'Services'), ('15', 'Services (FED in ST Mode)'), ('16', 'Processing/Conversion of Goods'), ('17', 'Special Procedure Goods'), ('18', 'Telecommunication services'), ('19', 'Petroleum Products'), ('20', 'MT'), ('21', 'Bill of lading'), ('22', 'SET'), ('23', 'KWH')], "Sale Type")
    schedule_no = fields.Selection([('1', '(549(I)/2008'),  ('2', '811(I)/2009'), ('3', 'Zero Rated Elec.'), ('4', 'Zero Rated Gas'), ('5', '5th Schedule'), ('6', '1125(I)/2011'), ('7', '608(I)/2012'), ('8', '79(I)/2012'), ('9', '1st Schedule FED'), ('10', '1007(I)/2005'), ('11', '326(I)/2008'), ('12', '539(I)/2008'), ('13', '542(I)/2008'), ('14', '551(I)/2008'), ('15', '727(I)/2011'), ('16', '76(I)/2008'), ('17', '880(I)/2007'), ('18', '6th Schd Table I'), ('19', '6th Schd Table II'), ('20', 'DTRE'), ('21', 'FED 3rd Schd Table I'), ('22', 'FED 3rd Schd Table II'), ('23', 'Section 4(b)'), ('24', '802(I)/2009'), ('25', '678(I)/2004'), ('26', '760(I)/2012'), ('27', '213(I)/2013'), ('28', '499(I)/2013'), ('29', '501(I)/2013'), ('30', '670(I)/2013'), ('31', '657(I)/2013'), ('32', '898(I)/2013'), ('33', '896(I)/2013'), ('34', '460(I)/2013')], "SRO No. / Schedule No.")
    item_sr_no = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31'),('32','32'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),('41','41'),('42','42'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),('50','50'),('51','51'),('52','52'),('53','53'),('54','54'),('55','55'),('56','56'),('57','57'),('58','58'),('59','59'),('60','60'),('61','61'),('62','62'),('63','63'),('64','64'),('65','65'),('66','66'),('67','67'),('68','68'),('69','69'),('70','70'),('71','71'),('72','72'),('73','73'),('74','74'),('75','75'),('76','76'),('77','77'),('78','78'),('79','79'),('80','80'),('81','81'),('82','82'),('83','83'),('84','84'),('85','85'),('86','86'),('87','87'),('88','88'),('89','89'),('90','90'),('91','91'),('92','92'),('93','93'),('94','94'),('95','95'),('96','96'),('97','97'),('98','98'),('99','99'),('100','100'),('101','101'),('102','102'),('103','103'),('104','104'),('105','105'),('106','106'),('107','107'),('108','108'),('109','109'),('110','110'),('111','111'),('112','112'),('113','113'),('114','114'),('115','115'),('116','116'),('117','117'),('118','118'),('119','119'),('120','120'),('121','121'),('122','122'),('123','123'),('124','124'),('125','125'),('126','126'),('127','127'),('128','128'),('129','A'),('130','B'),('131','C'),('132','52A')], "Item Sr. No.")
    x_rate = fields.Selection([('1', '17'),  ('2', '2'), ('3', '3'), ('4', '5'), ('5', '7.5'), ('6', '8'), ('7', '10'), ('8', '16'), ('9', '18.5'), ('10', '0'), ('11', '0.5'), ('12', 'Exempt'), ('13', 'DTRE'), ('14', 'Rs.7/KWH'), ('15', '6700-MT'), ('16', 'Rs.1/kg'), ('17', 'Rs. 8/KWH'), ('18', 'Rs. 250/SIM'), ('19', 'Rs.500/IMEI'), ('20', 'Rs.250/IMEI'),('21', 'Rs.150/IMEI'),('22', '22'),('23', '27'),('24', '18'),('25', '32'),('26', '37')], "Rate")
    x_hs_code = fields.Float(string="HS Code")
    x_description = fields.Selection([('1', '85-03-ELECTRIC MACHINERY HOME APPLIANCES'),('2', '94-01-FURNITURE; BEDDING, MATTRESSES, MATTRESS '),('3', '85-03-ELECTRIC MACHINERY HOME APPLIANCES ELECTRIC')],string="Description")

class tax_customizations_account_invoice_line(models.Model):
    _inherit = "account.invoice.line"
    
    sale_type = fields.Selection([('1', 'Goods at standard rate'),  ('2', 'Third Schedule Goods'), ('3', 'Good at Reduced Rate'), ('4', 'Electricity Supply to Retailers'), ('5', 'Electricity to stell sector'), ('6', 'Gas to CNG stations'), ('7', 'Re-rollable scrap by ship-breakers'), ('8', 'SIM sale / IMEI activation'), ('9', 'Goods (FED in ST Mode)'), ('10', 'Goods at zero-rate'), ('11', 'Exempt goods'), ('12', 'Other'), ('13', 'DTRE goods'), ('14', 'Services'), ('15', 'Services (FED in ST Mode)'), ('16', 'Processing/Conversion of Goods'), ('17', 'Special Procedure Goods'), ('18', 'Telecommunication services'), ('19', 'Petroleum Products'), ('20', 'MT'), ('21', 'Bill of lading'), ('22', 'SET'), ('23', 'KWH')], "Sale Type")
    schedule_no = fields.Selection([('1', '(549(I)/2008'),  ('2', '811(I)/2009'), ('3', 'Zero Rated Elec.'), ('4', 'Zero Rated Gas'), ('5', '5th Schedule'), ('6', '1125(I)/2011'), ('7', '608(I)/2012'), ('8', '79(I)/2012'), ('9', '1st Schedule FED'), ('10', '1007(I)/2005'), ('11', '326(I)/2008'), ('12', '539(I)/2008'), ('13', '542(I)/2008'), ('14', '551(I)/2008'), ('15', '727(I)/2011'), ('16', '76(I)/2008'), ('17', '880(I)/2007'), ('18', '6th Schd Table I'), ('19', '6th Schd Table II'), ('20', 'DTRE'), ('21', 'FED 3rd Schd Table I'), ('22', 'FED 3rd Schd Table II'), ('23', 'Section 4(b)'), ('24', '802(I)/2009'), ('25', '678(I)/2004'), ('26', '760(I)/2012'), ('27', '213(I)/2013'), ('28', '499(I)/2013'), ('29', '501(I)/2013'), ('30', '670(I)/2013'), ('31', '657(I)/2013'), ('32', '898(I)/2013'), ('33', '896(I)/2013'), ('34', '460(I)/2013')], "SRO No. / Schedule No.")
    item_sr_no = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31'),('32','32'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),('41','41'),('42','42'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),('50','50'),('51','51'),('52','52'),('53','53'),('54','54'),('55','55'),('56','56'),('57','57'),('58','58'),('59','59'),('60','60'),('61','61'),('62','62'),('63','63'),('64','64'),('65','65'),('66','66'),('67','67'),('68','68'),('69','69'),('70','70'),('71','71'),('72','72'),('73','73'),('74','74'),('75','75'),('76','76'),('77','77'),('78','78'),('79','79'),('80','80'),('81','81'),('82','82'),('83','83'),('84','84'),('85','85'),('86','86'),('87','87'),('88','88'),('89','89'),('90','90'),('91','91'),('92','92'),('93','93'),('94','94'),('95','95'),('96','96'),('97','97'),('98','98'),('99','99'),('100','100'),('101','101'),('102','102'),('103','103'),('104','104'),('105','105'),('106','106'),('107','107'),('108','108'),('109','109'),('110','110'),('111','111'),('112','112'),('113','113'),('114','114'),('115','115'),('116','116'),('117','117'),('118','118'),('119','119'),('120','120'),('121','121'),('122','122'),('123','123'),('124','124'),('125','125'),('126','126'),('127','127'),('128','128'),('129','A'),('130','B'),('131','C'),('132','52A')], "Item Sr. No.")
    x_rate = fields.Selection([('1', '17'),  ('2', '2'), ('3', '3'), ('4', '5'), ('5', '7.5'), ('6', '8'), ('7', '10'), ('8', '16'), ('9', '18.5'), ('10', '0'), ('11', '0.5'), ('12', 'Exempt'), ('13', 'DTRE'), ('14', 'Rs.7/KWH'), ('15', '6700-MT'), ('16', 'Rs.1/kg'), ('17', 'Rs. 8/KWH'), ('18', 'Rs. 250/SIM'), ('19', 'Rs.500/IMEI'), ('20', 'Rs.250/IMEI'),('21', 'Rs.150/IMEI'),('22', '22'),('23', '27'),('24', '18'),('25', '32'),('26', '37')], "Rate")
    x_hs_code = fields.Float(string="HS Code")
    x_description = fields.Selection([('1', '85-03-ELECTRIC MACHINERY HOME APPLIANCES'),('2', '94-01-FURNITURE; BEDDING, MATTRESSES, MATTRESS '),('3', '85-03-ELECTRIC MACHINERY HOME APPLIANCES ELECTRIC')],string="Description")
    
class tax_customizations_account_tax(models.Model):
    _inherit = "account.invoice.tax"
    
    sale_type = fields.Selection([('1', 'Goods at standard rate'),  ('2', 'Third Schedule Goods'), ('3', 'Good at Reduced Rate'), ('4', 'Electricity Supply to Retailers'), ('5', 'Electricity to stell sector'), ('6', 'Gas to CNG stations'), ('7', 'Re-rollable scrap by ship-breakers'), ('8', 'SIM sale / IMEI activation'), ('9', 'Goods (FED in ST Mode)'), ('10', 'Goods at zero-rate'), ('11', 'Exempt goods'), ('12', 'Other'), ('13', 'DTRE goods'), ('14', 'Services'), ('15', 'Services (FED in ST Mode)'), ('16', 'Processing/Conversion of Goods'), ('17', 'Special Procedure Goods'), ('18', 'Telecommunication services'), ('19', 'Petroleum Products'), ('20', 'MT'), ('21', 'Bill of lading'), ('22', 'SET'), ('23', 'KWH')], "Sale Type")
    schedule_no = fields.Selection([('1', '(549(I)/2008'),  ('2', '811(I)/2009'), ('3', 'Zero Rated Elec.'), ('4', 'Zero Rated Gas'), ('5', '5th Schedule'), ('6', '1125(I)/2011'), ('7', '608(I)/2012'), ('8', '79(I)/2012'), ('9', '1st Schedule FED'), ('10', '1007(I)/2005'), ('11', '326(I)/2008'), ('12', '539(I)/2008'), ('13', '542(I)/2008'), ('14', '551(I)/2008'), ('15', '727(I)/2011'), ('16', '76(I)/2008'), ('17', '880(I)/2007'), ('18', '6th Schd Table I'), ('19', '6th Schd Table II'), ('20', 'DTRE'), ('21', 'FED 3rd Schd Table I'), ('22', 'FED 3rd Schd Table II'), ('23', 'Section 4(b)'), ('24', '802(I)/2009'), ('25', '678(I)/2004'), ('26', '760(I)/2012'), ('27', '213(I)/2013'), ('28', '499(I)/2013'), ('29', '501(I)/2013'), ('30', '670(I)/2013'), ('31', '657(I)/2013'), ('32', '898(I)/2013'), ('33', '896(I)/2013'), ('34', '460(I)/2013')], "SRO No. / Schedule No.")
    item_sr_no = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31'),('32','32'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),('41','41'),('42','42'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),('50','50'),('51','51'),('52','52'),('53','53'),('54','54'),('55','55'),('56','56'),('57','57'),('58','58'),('59','59'),('60','60'),('61','61'),('62','62'),('63','63'),('64','64'),('65','65'),('66','66'),('67','67'),('68','68'),('69','69'),('70','70'),('71','71'),('72','72'),('73','73'),('74','74'),('75','75'),('76','76'),('77','77'),('78','78'),('79','79'),('80','80'),('81','81'),('82','82'),('83','83'),('84','84'),('85','85'),('86','86'),('87','87'),('88','88'),('89','89'),('90','90'),('91','91'),('92','92'),('93','93'),('94','94'),('95','95'),('96','96'),('97','97'),('98','98'),('99','99'),('100','100'),('101','101'),('102','102'),('103','103'),('104','104'),('105','105'),('106','106'),('107','107'),('108','108'),('109','109'),('110','110'),('111','111'),('112','112'),('113','113'),('114','114'),('115','115'),('116','116'),('117','117'),('118','118'),('119','119'),('120','120'),('121','121'),('122','122'),('123','123'),('124','124'),('125','125'),('126','126'),('127','127'),('128','128'),('129','A'),('130','B'),('131','C'),('132','52A')], "Item Sr. No.")
    x_rate = fields.Selection([('1', '17'),  ('2', '2'), ('3', '3'), ('4', '5'), ('5', '7.5'), ('6', '8'), ('7', '10'), ('8', '16'), ('9', '18.5'), ('10', '0'), ('11', '0.5'), ('12', 'Exempt'), ('13', 'DTRE'), ('14', 'Rs.7/KWH'), ('15', '6700-MT'), ('16', 'Rs.1/kg'), ('17', 'Rs. 8/KWH'), ('18', 'Rs. 250/SIM'), ('19', 'Rs.500/IMEI'), ('20', 'Rs.250/IMEI'),('21', 'Rs.150/IMEI'),('22', '22'),('23', '27'),('24', '18'),('25', '32'),('26', '37')], "Rate")
    x_hs_code = fields.Float(string="HS Code")
    x_description = fields.Selection([('1', '85-03-ELECTRIC MACHINERY HOME APPLIANCES'),('2', '94-01-FURNITURE; BEDDING, MATTRESSES, MATTRESS '),('3', '85-03-ELECTRIC MACHINERY HOME APPLIANCES ELECTRIC')],string="Description")
    
    @api.v8
    def compute(self, invoice):
        tax_grouped = {}
        currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))
        company_currency = invoice.company_id.currency_id
        for line in invoice.invoice_line:

            unit_price = line.price_unit

            if line.item_seller_price != 0:
                unit_price = line.item_seller_price
                
            taxes = line.invoice_line_tax_id.compute_all(
                (unit_price * (1 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, invoice.partner_id)['taxes']
            for tax in taxes:
                val = {
                    'invoice_id': invoice.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'manual': False,
                    'sequence': tax['sequence'],
                    'base': currency.round(tax['price_unit'] * line['quantity']),
                    

                }
                if invoice.type in ('out_invoice','in_invoice'):
                    taxes_obj = self.env['account.tax'].search([('name','=',tax['name'])])[0]
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['sale_type'] = taxes_obj.sale_type
                    val['schedule_no'] = taxes_obj.schedule_no
                    val['item_sr_no'] = taxes_obj.item_sr_no
                    val['x_rate'] = taxes_obj.x_rate
                    val['x_hs_code'] = taxes_obj.x_hs_code
                    val['x_description'] = taxes_obj.x_description
                    val['base_amount'] = currency.compute(val['base'] * tax['base_sign'], company_currency, round=False)
                    val['tax_amount'] = currency.compute(val['amount'] * tax['tax_sign'], company_currency, round=False)
                    val['account_id'] = tax['account_collected_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_collected_id']
                else:
                    taxes_obj = self.env['account.tax'].search([('name','=',tax['name'])])[0]
                    val['sale_type'] = taxes_obj.sale_type
                    val['schedule_no'] = taxes_obj.schedule_no
                    val['item_sr_no'] = taxes_obj.item_sr_no
                    val['x_rate'] = taxes_obj.x_rate
                    val['x_hs_code'] = taxes_obj.x_hs_code
                    val['x_description'] = taxes_obj.x_description
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = currency.compute(val['base'] * tax['ref_base_sign'], company_currency, round=False)
                    val['tax_amount'] = currency.compute(val['amount'] * tax['ref_tax_sign'], company_currency, round=False)
                    val['account_id'] = tax['account_paid_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_paid_id']

                # If the taxes generate moves on the same financial account as the invoice line
                # and no default analytic account is defined at the tax level, propagate the
                # analytic account from the invoice line to the tax line. This is necessary
                # in situations were (part of) the taxes cannot be reclaimed,
                # to ensure the tax move is allocated to the proper analytic account.
                if not val.get('account_analytic_id') and line.account_analytic_id and val['account_id'] == line.account_id.id:
                    val['account_analytic_id'] = line.account_analytic_id.id

                key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                if not key in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
            t['base_amount'] = currency.round(t['base_amount'])
            t['tax_amount'] = currency.round(t['tax_amount'])

        return tax_grouped
