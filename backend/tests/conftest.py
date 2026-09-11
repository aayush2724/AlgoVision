import os

# Must be set before app modules import — their rate limiters read it at
# import time. The test suite fires hundreds of requests per minute from one
# client, which would otherwise trip the per-IP limits with 429s.
os.environ["ALGOVISION_DISABLE_RATELIMIT"] = "1"
