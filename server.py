import os
import sys

port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    from jobcert import app
    app.run(host='0.0.0.0', port=port, debug=True)