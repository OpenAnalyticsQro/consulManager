import requests
import shutil
from pathlib import Path

zpl_code = '^xa^cfa,50^fo100,100^fdHello World^fs^xz'
API_LABERY_POST = "http://api.labelary.com/v1/printers/{dpmm}/labels/{label_size}/{index}/{zpl}"

# The desired print density, in dots per millimeter.
DPM_VALUES = {"6 dpmm (152 dpi)": "6dpmm",
              "8 dpmm (203 dpi)": "8dpmm",
              "12 dpmm (300 dpi)": "12dpmm",
              "24 dpmm (600 dpi)": "24dpmm",  }

# The available label width
LABEL_SIZE_VALUES = {"4x6 inches": "4x6",
                    "4x8 inches": "4x8"}

# The label index (base 0).
LABEL_INDEX_DEFUALT = 0

# The ZPL code to render.
ZPL_CODE_RENDER_DEFUALT = ""

def request_new_label(dpmm=DPM_VALUES["8 dpmm (203 dpi)"], label_size=LABEL_SIZE_VALUES["4x8 inches"], index=LABEL_INDEX_DEFUALT, zpl=ZPL_CODE_RENDER_DEFUALT, zpl_code=None, out_path=None):
    # url = 'http://api.labelary.com/v1/printers/8dpmm/labels/4x6/0/'
    url = f"http://api.labelary.com/v1/printers/{dpmm}/labels/{label_size}/{index}/{zpl}"
    files = {'file' : zpl_code}
    headers = {'Accept' : 'application/pdf'} # omit this line to get PNG images back
    response = requests.post(url, headers = headers, files = files, stream = True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open(out_path, 'wb') as fd: # change file name for PNG images
            shutil.copyfileobj(response.raw, fd)
    else:
        print('Error: ' + response.text)

if __name__ == "__main__":
    out_path = Path(r"C:\Users\diana\Documents\Hirvin\ConsulManager\consulManager\ConsulManager\mercadoZPL\test.pdf")
    request_new_label(zpl_code=zpl_code, out_path=out_path)