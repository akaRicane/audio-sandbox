npm run dev &
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        ./venv/bin/python3.9 ./audiogui/project/app.py
elif [[ "$OSTYPE" == "darwin"* ]]; then
        ./venv/bin/python3.9 ./audiogui/project/app.py
elif [[ "$OSTYPE" == "msys"* ]] ; then
        ./venv/Scripts/python.exe ./audiogui/project/app.py
else
    echo "Audio Gui run failed !! Ask Pascal"
fi
echo "Running !"
echo "Go to `http://127.0.0.1:5000/` page in web browser"