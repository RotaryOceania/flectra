###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies (<https://gitlab.com/flectra-community/flectra>).
#    Author: Cybrosys Techno Solutions, Jamotion GmbH (<https://gitlab.com/flectra-community/flectra>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

{
    'name': 'Employee Dynamic Fields',
    'version': '1.0.1.0.0',
    'summary': """Ability To Add Custom Fields in Employee From User Level""",
    'description': """Ability To Add Custom Fields in Employee From User Level,Employee Custom Fields,
                      Employee Dynamic Fields, flectra13, Dynamic Employee Fields, Dynamic Fields, Create Dynamic Fields, Community flectra Studio""",
    'category': 'Extra Tools',
    'author': 'Cybrosys Techno Solutions, Jamotion GmbH',
    'company': 'Cybrosys Techno Solutions, Jamotion GmbH',
    'maintainer': 'Cybrosys Techno Solutions, Jamotion GmbH',
    'website': "https://gitlab.com/flectra-community/flectra",
    'depends': ['hr'],
    'data': [
        'data/widget_data.xml',
        'security/ir.model.access.csv',
        'security/employee_security_group.xml',
        'wizard/employee_fields_view.xml',
        'views/ir_fields_search_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
