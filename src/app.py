import os
import utils as ut
import contents

def create_hexagonal_structure(name_project, local):
    os.chdir(local)
    ut.create_folder(name_project)
    os.chdir(name_project)
    os.system('npm init')
    os.system('npm install express dotenv mongodb debug')
    os.system('npm install -D jest eslint')
    os.system('git init')

    # folders source
    ut.create_folder('src')
    ut.create_folder('tests')
    ut.create_folder('.vscode')
    ut.create_file('.gitignore', contents.gitignore)

    # src
    os.chdir('src')
    ut.create_folder('bin')
    ut.create_folder('domain')
    ut.create_folder('infrastructure')
    ut.create_folder('interfaces')
    ut.create_folder('useCases')

    # bin
    os.chdir('bin')
    ut.create_file('www', contents.www)

    # domain
    os.chdir('..')
    os.chdir('domain')
    ut.create_folder('user')
    os.chdir('user')
    ut.create_file('index.js', contents.domain_user_index)
    ut.create_file('userDomain.js', contents.domain_user_user_domain)
    ut.create_file('userValidate.js', contents.domain_user_validate)

    # infrastructure
    os.chdir('..')
    os.chdir('..')
    os.chdir('infrastructure')
    ut.create_folder('user')
    os.chdir('user')
    ut.create_folder('db')
    ut.create_folder('webserver')
    os.chdir('db')
    ut.create_file('index.js', contents.infrastructure_user_db)
    os.chdir('..')
    os.chdir('webserver')
    ut.create_file('routes.js', contents.infrastructure_user_webserver_routes)
    ut.create_file('index.js', contents.infrastructure_user_webserver_index)

    # interfaces
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    os.chdir('interfaces')
    ut.create_folder('user')
    os.chdir('user')
    ut.create_folder('controllers')
    ut.create_folder('data-access')
    ut.create_folder('express-callback')
    os.chdir('controllers')
    ut.create_file('index.js', contents.interfaces_user_controllers_index)
    ut.create_file('user-post.js', contents.interfaces_user_controllers_post)
    os.chdir('..')
    os.chdir('data-access')
    ut.create_file('index.js', contents.interfaces_user_data_access_index)
    ut.create_file('user-db.js', contents.interfaces_user_data_access_user_db)
    os.chdir('..')
    os.chdir('express-callback')
    ut.create_file('index.js', contents.interfaces_user_express_callback)

    # useCases
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    os.chdir('useCases')
    ut.create_folder('user')
    os.chdir('user')
    ut.create_file('index.js', contents.use_cases_user_index)
    ut.create_file('createUser.js', contents.use_cases_user_create)

    # tests
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    os.chdir('tests')
    ut.create_folder('unit')
    os.chdir('unit')
    ut.create_folder('domain')
    ut.create_folder('interfaces')
    ut.create_folder('useCases')
