import os
import asyncio
import logging
from ..lib.ecmwf_client import ECMWFClient
from ..lib.neuralgcm_wrapper import NeuralGCMWrapper

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.use_neuralgcm = os.getenv("USE_NEURALGCM", "false").lower() == "true"
        self.ecmwf = ECMWFClient() if not self.use_neuralgcm else None
        self.gcm = NeuralGCMWrapper() if self.use_neuralgcm else None

    async def enhance_forecast(self, lat: float, lon: float):
        """Get enhanced forecast from selected backend"""
        try:
            if self.use_neuralgcm:
                # Run synchronous NeuralGCM code in thread pool
                return await asyncio.to_thread(
                    self._neuralgcm_prediction, 
                    lat, 
                    lon
                )
            return await self._ecmwf_prediction(lat, lon)
        except Exception as e:
            logger.error(f"Enhancement failed: {str(e)}")
            return {"error": str(e), "source": "none"}

    def _neuralgcm_prediction(self, lat: float, lon: float):
        """Synchronous wrapper for NeuralGCM"""
        try:
            return {
                "source": "NeuralGCM",
                **self.gcm.predict(lat, lon)
            }
        except Exception as e:
            logger.error(f"NeuralGCM prediction failed: {str(e)}")
            return {"error": str(e), "source": "NeuralGCM"}

    async def _ecmwf_prediction(self, lat: float, lon: float):
        """Async ECMWF prediction"""
        try:
            return {
                "source": "ECMWF",
                **await self.ecmwf.get_wind_data(lat, lon)
            }
        except Exception as e:
            logger.error(f"ECMWF prediction failed: {str(e)}")
            return {"error": str(e), "source": "ECMWF"}
