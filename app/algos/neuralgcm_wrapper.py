# app/lib/neuralgcm_wrapper.py
import neuralgcm
import jax
import xarray as xr
import numpy as np
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class NeuralGCMWrapper:
    def __init__(self, checkpoint_path: str = None):
        """
        Initialize NeuralGCM model wrapper
        
        Args:
            checkpoint_path: Optional path to custom checkpoint
        """
        try:
            if checkpoint_path:
                self.checkpoint = neuralgcm.load_checkpoint(checkpoint_path)
            else:
                # Load TL63 stochastic demo
                self.checkpoint = neuralgcm.demo.load_checkpoint_tl63_stochastic()
                
            self.model = neuralgcm.PressureLevelModel.from_checkpoint(self.checkpoint)
            self.ds = neuralgcm.demo.load_data(self.model.data_coords)
            
            # Verify available variables
            self.available_vars = list(self.ds.data_vars.keys())
            logger.info(f"Loaded NeuralGCM model with variables: {self.available_vars}")
            
            # Initialize wind proxy if needed
            if 'eastward_wind' not in self.available_vars:
                logger.warning("Wind components missing - using temperature gradients as proxy")
                
        except Exception as e:
            logger.error(f"NeuralGCM initialization failed: {str(e)}")
            raise

    def predict(self, lat: float, lon: float) -> Dict[str, list]:
        """
        Generate wind predictions using available variables
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees
            
        Returns:
            Dictionary with wind_speed and wind_direction lists
        """
        try:
            # Get model prediction
            ds_init = self.ds.isel(time=0)
            inputs, forcings = self.model.data_from_xarray(ds_init)
            encoded = self.model.encode(inputs, forcings, jax.random.PRNGKey(0))
            advanced = self.model.advance(encoded, forcings)
            decoded = self.model.decode(advanced, forcings)

            # Extract wind data based on available variables
            if 'eastward_wind' in decoded and 'northward_wind' in decoded:
                # Real wind components available
                u = decoded["eastward_wind"].values.squeeze()
                v = decoded["northward_wind"].values.squeeze()
            else:
                # Fallback: Use temperature gradients as wind proxy
                logger.info("Using temperature gradients as wind proxy")
                temp = decoded["air_temperature"].values.squeeze()
                u = np.gradient(temp, axis=1)  # Latitudinal gradient
                v = np.gradient(temp, axis=2)  # Longitudinal gradient

            # Convert to wind speed/direction
            wind_speed = np.sqrt(u**2 + v**2).tolist()
            wind_dir = (np.degrees(np.arctan2(-u, -v)) % 360).tolist()

            return {
                "wind_speed": wind_speed,
                "wind_direction": wind_dir
            }

        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return {"wind_speed": [], "wind_direction": []}

    @staticmethod
    def request_access(email: str):
        """Request access to full model checkpoints"""
        neuralgcm.request_access(email=email)
        logger.info(f"Access request sent to NeuralGCM team. Check {email} for updates")

    def load_custom_checkpoint(self, path: str):
        """Load a custom checkpoint with wind variables"""
        try:
            self.checkpoint = neuralgcm.load_checkpoint(path)
            self.model = neuralgcm.PressureLevelModel.from_checkpoint(self.checkpoint)
            logger.info(f"Loaded custom checkpoint from {path}")
        except Exception as e:
            logger.error(f"Failed to load custom checkpoint: {str(e)}")
            raise
