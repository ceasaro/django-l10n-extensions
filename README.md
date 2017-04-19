# about-py
Django about plugin

Makes a webpage available with information about the projects last version control system commits and
 the python interpreter and used python libraries.
 
# How to use
 1. `pip install about-py`
 2. add about-py to your Django INSTALLED_APPS:<br/>
   <pre><code>INSTALLED_APPS = [
      ...,
      about-py,
      ...,
   ]</code></pre>
 3. Create an url entry with the `AboutView`. e.g.<br/>
  <pre><code>
      url(r'^about/', AboutView.as_view()),
  </code></pre><br/>
  Or use the secure `SecureAboutView` so only staff and super users can access the page.
