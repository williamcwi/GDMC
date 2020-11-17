import json

displayName = "Settlement Generator"

inputs = [
    (
        ('Settlement Generator', 'title'),
        
        ('By William, Selina, Ho Kiu, Rhys', 'label'),
        ('', 'label'),
    )
]

def perform(level, box, options):
    print('Starting Generation...')

    try:
        path_to_file = "C:\\Users\\selin\\OneDrive\\Documents\\MCEdit\\Filters"
        file_name = "platform"
        file_path = "{}\\templates\\house1\\{}.json".format(path_to_file, file_name)
        print('Loading JSON template from {}...'.format(file_path))
        template = loadFile(file_path)
        print('Template loaded')

    except Exception as e:
        print(e)

    print('Placing blocks in template...')
    for block in template:
        block_id = block['id']
        block_data = block['data']
        block_x = block['x'] + box.minx
        block_y = block['y'] + box.miny
        block_z = block['z'] + box.minz

        level.setBlockAt(block_x, block_y, block_z, block_id)
        level.setBlockDataAt(block_x, block_y, block_z, block_data)

def loadFile(file_path):
    with open(file_path) as f:
        return json.load(f)