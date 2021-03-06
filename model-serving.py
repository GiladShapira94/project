import mlrun
import os

import numpy as np
from cloudpickle import load

class LGBMModel(mlrun.serving.V2ModelServer):
    
    def load(self):
        model_file, extra_data = self.get_model('.pkl')
        self.model = load(open(model_file, 'rb'))

    def predict(self, body):
        try:
            feats = np.asarray(body['inputs'])
            result = self.model.predict(feats)
            return result.tolist()
        except Exception as e:
            raise Exception("Failed to predict %s" % e)


from mlrun.runtimes import nuclio_init_hook
def init_context(context):
    nuclio_init_hook(context, globals(), 'serving_v2')

def handler(context, event):
    return context.mlrun_handler(context, event)
