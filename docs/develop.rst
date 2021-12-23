Develop
=========

In order to add a new template model ``<my_new_template>`` the following steps need to be done:

1.  Create a new folder named ``__cc_<my_new_template>`` in ``{{cookiecutter.directory_name}}`` containing
    the relative ``cookiecutter.json`` file and a ``{{cookiecutter._simple_placeholder}}`` directory which
    should be filled with the template-specific content:
    .. code-block::

      {{cookiecutter.directory_name}}
      ├── __cc_<my_new_template>
      │   ├── cookiecutter.json
      │   └── {{cookiecutter._simple_placeholder}}
      │       └── ...
      └── ...

    .. note::
      The directory ``{{cookiecutter._simple_placeholder}}`` is needed to be able to use the
      associated ``cookiecutter.json`` file.

    .. note::
      If a file already exists in  ``{{cookiecutter.directory_name}}``
      it will be **overwritten** by the new template

    .. note::
      All the files and folders, in  ``{{cookiecutter.directory_name}}``, starting with a double underscore (``__cc_``) will be removed once
      the project has been created.

2. Enable the new template adding the ``<my_new_template>`` entry to the ``project_type`` section in the main ``cookiecutter.json`` file.
   
  .. note::
    By default, the template name in ``project_type`` should match the directory name. Alternatively you can add the right 
    association to the ``map_choice_dir`` variable in ``hooks/post_gen_project.py``:

    .. code-block:: python

      map_choice_dir = {
          'FastAPI': 'fastAPI',
          'Base': 'base',
          'Streamlit': 'streamlit',
     }
