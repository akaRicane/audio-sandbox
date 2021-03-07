npm install
# TODO code may won't work if python path link to python version not supported
# User should specify version
python -m venv venv

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        source venv/bin/activate
elif [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
elif [[ "$OSTYPE" == "msys"* ]] ; then
        source venv/Scripts/activate
else
    echo "Install failed !! Ask Pascal"

fi
echo "Install is a success ! Processing packages ..."
pip install wheel
pip install -r requirements.txt
pipwin install pyaudio
echo "Packages installed ! Please run: sh.runserver.sh"