import bmp
# to make font file: python make_font.py -f /usr/share/fonts/truetype/msttcorefonts/arialbd.ttf -s 12
import bmpfont_arial_12
from PIL import Image
import json
import uuid

flag = 'gccctf{workflow_restored}'.upper()

# Create single-pixel width letters
text_img = bmp.BitMap(len(flag)*8,20,bmp.Color.WHITE)
text_img.setFont(bmpfont_arial_12.font_data)
text_img.setPenColor( bmp.Color.BLACK )
text_img.drawText(flag, 0, 0)
text_img.saveFile('output.bmp')

# Convert to workflow
img = Image.open('output.bmp')
pixels = img.load()
(w,h)=img.size

with open('flag.ga', 'w') as wf:
    preamble = [
    '{\n"a_galaxy_workflow": "true"',
    '"annotation": ""',
    '"format-version": "0.1"',
    '"name": "Picasso\'s Pipeline II"',
    '"steps": {\n']

    wf.writelines(',\n'.join(preamble))

    count = -1
    steps = []
    for j in range(0,h):
        for i in range(0,w):
            (r,g,b) = pixels[i,j]
            if r == 0:
                count+=1
                left = 100+i*50
                top = 150+j*50
                step = [
                '"'+str(count)+'": {',
                '    "annotation": "",',
                '    "content_id": null,',
                '    "id": '+str(count)+',',
                '    "input_connections": {},',
                '    "inputs": [',
                '        {',
                '            "description": "",',
                '            "name": "Input Dataset"',
                '        }',
                '    ],',
                '    "label": null,',
                '    "name": "Input dataset",',
                '    "outputs": [],',
                '    "position": {',
                '        "left": '+str(left)+',',
                '        "top": '+str(top),
                '    },',
                '    "tool_errors": null,',
                '    "tool_id": null,',
                '    "tool_state": "{\\"name\\": \\"Input Dataset\\"}",',
                '    "tool_version": null,',
                '    "type": "data_input",',
                '    "uuid": "'+str(uuid.uuid4())+'",',
                '    "workflow_outputs": []',
                '}'
                ]
                steps.append('\n'.join(step))

    wf.write(',\n'.join(steps))
    postamble = [ '},', '"uuid": "'+str(uuid.uuid4())+'"',  '}' ]
    wf.writelines('\n'.join(postamble))
