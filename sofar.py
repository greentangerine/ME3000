from flask import Flask, render_template
import sys

sys.path.insert(0, '/home/pi/ME3000')
import ME3000 as me

app = Flask(__name__)

THRESHOLD_FILE="/home/pi/ME3000/pct.txt"

def read_threshold():
    try:
        tfile = open(THRESHOLD_FILE, "r")
        threshold = int(tfile.readline().split("=")[-1])
        tfile.close()
    except:
        threshold = -1
    return threshold


def write_threshold(pctval):
    if pctval >=20 and pctval <= 100:
        try:
            ostr = "THRESHOLD=" + str(pctval)
            print(ostr)
            tfile = open(THRESHOLD_FILE, "w")
            tfile.write(ostr)
            tfile.close()
            return pctval
        except:
            return -1
    else:
        return -1


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pct/')
@app.route('/pct/<int:pct_val>')
def set_pct(pct_val=None):
    if pct_val == None:
        retval = read_threshold()
        if retval != -1:
            return render_template('pct.html', opstr="Current", pctval=retval) 
        else:
             return render_template('error.html'), 500
    else:
        retval = write_threshold(pct_val)
        if retval != -1:
            return render_template('pct.html', opstr="New", pctval=retval) 
        else:
             return render_template('error.html'), 500
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

