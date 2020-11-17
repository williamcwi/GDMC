import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('Generate Settlement')

inputs = [
    (
        ('Settlement Generator', 'title'),
        
        ('By William, Selina, Ho Kiu, Rhys', 'label'),
        ('', 'label'),

    ),
    (
        ('Settlement Settings', 'title'),
        (),
    )
]

def perform(level, box, options):
