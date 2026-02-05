from investiq.data.historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from investiq.data.historical_data_engine.request.IBKRRequestSettings import IBKRRequestSettings

class HistoricalRequestBuilder:
    @staticmethod
    def build(
            instrument: InstrumentSettings,
            request_settings: IBKRRequestSettings
    ) -> dict:
        contract = instrument.to_contract()
        completed_request = request_settings.with_defaults_from(instrument)
        return completed_request.to_query_kwargs(contract)