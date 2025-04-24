# Studyroom
<h2>Setting up the environment</h2>
<ol>
  <li>Install python 3.10.4</li>
  <a href="https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe">Download python</a>
  <li>Install virtual environment wrapper in cmd:  </li>
  <p>pip install virtualenvwrapper-win</p>
  <li>create virtual environment called 'env' in cmd:</li>
  <p>mkvirtualenv env</p>
  <li> Install django in your environment 'env' </li>
  <p>pip install django</p>
  </ol>
  <h2>installing other packages</h2>
  <ul>
   <li>Install requirement</li>
   <p>pip install -r requirements.txt</p>
   </ul> 
   <h2>Running the project</h2>
   <ol>
  <li>open the project folder in VS code or in cmd</li>
  <li> activate the environment with below command</li>
  <p>workon env</p>
  <li>make migration</li>
  <p>python manage.py migrate</p>
  <li>run the server with below command:</li>
  <p>python manage.py runserver</p>
  </ol>