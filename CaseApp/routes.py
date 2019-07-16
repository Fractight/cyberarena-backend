from .app import api
from .resources.CaseInfo import CaseInfo
from .resources.CasesInfo import CasesInfo
from .resources.CaseOpen import CaseOpen
from .resources.ItemsInfo import ItemsInfo
from .resources.ItemActivate import ItemActivate


api.add_resource(CasesInfo, '/cases')
api.add_resource(CaseInfo, '/cases/<int:case_id>')
api.add_resource(CaseOpen, '/cases/<int:case_id>')
api.add_resource(ItemsInfo, '/items')
api.add_resource(ItemActivate, '/items/<int:item_id>')