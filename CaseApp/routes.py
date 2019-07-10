from .app import api
from .resources.ItemInfo import ItemInfo
from .resources.CaseInfo import CaseInfo
from .resources.CasesInfo import CasesInfo
from .resources.CaseOpen import CaseOpen
from .resources.Inventory import InventoryResource
from .resources.ItemActivate import ItemActivate

api.add_resource(ItemInfo, '/item')
api.add_resource(ItemActivate, '/item/activate/<int:item_id>')
api.add_resource(CaseInfo, '/case')
api.add_resource(CasesInfo, '/case/<int:case_id>')
api.add_resource(CaseOpen, '/case/open/<int:case_id>')
api.add_resource(InventoryResource, '/user/inventory')