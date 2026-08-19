from .goldprice_bars import GoldPriceDevBars
from .twelvedata_xau import TwelveDataXAUUSD
from .ice_dxy_delayed import ICEDXYDelayedPublic
from .ice_dxy_data_api import ICEDXYDataAPI
PROVIDERS={'GOLDPRICEDEV_XAU_BARS':GoldPriceDevBars,'TWELVEDATA_XAUUSD':TwelveDataXAUUSD,'ICE_DXY_DELAYED_PUBLIC':ICEDXYDelayedPublic,'ICE_DXY_DATA_API':ICEDXYDataAPI}
def instantiate(provider_id):return PROVIDERS[provider_id]()
