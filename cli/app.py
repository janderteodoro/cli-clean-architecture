import os
import utils as ut
import contents

def create_hexagonal_structure(name_project, local, database):
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
    ut.create_folder('adapters')
    ut.create_folder('bin')
    ut.create_folder('entitie')
    ut.create_folder('infrastructure')
    ut.create_folder('useCases')
    ut.create_folder('utils')

    # database error
    os.chdir('utils')
    ut.create_file('databaseError.js', contents.util_database_error)

    # bin
    os.chdir('..')
    os.chdir('bin')
    ut.create_file('www', contents.www)

    # domain
    os.chdir('..')
    os.chdir('entitie')
    ut.create_folder('user')
    os.chdir('user')
    ut.create_file('index.js', contents.user_entitie_index)
    ut.create_file('userEntitie.js', contents.user_entitie)
    ut.create_file('userValidate.js', contents.entitie_user_validate)

    # infrastructure
    if (database == 'MySQL'):
        os.chdir('..')
        os.chdir('..')
        os.chdir('infrastructure')
        ut.create_folder('user')
        os.chdir('user')
        ut.create_folder('db')
        ut.create_folder('webserver')
        os.chdir('db')
        ut.create_file('index.js', contents.infrastructure_user_db_mysql)
        os.chdir('..')
        os.chdir('webserver')
        ut.create_file('routes.js', contents.infrastructure_user_webserver_routes)
        ut.create_file('index.js', contents.infrastructure_user_webserver_index)
    else:
        os.chdir('..')
        os.chdir('..')
        os.chdir('infrastructure')
        ut.create_folder('user')
        os.chdir('user')
        ut.create_folder('db')
        ut.create_folder('webserver')
        os.chdir('db')
        ut.create_file('index.js', contents.infrastructure_user_db_mongo)
        os.chdir('..')
        os.chdir('webserver')
        ut.create_file('routes.js', contents.infrastructure_user_webserver_routes)
        ut.create_file('index.js', contents.infrastructure_user_webserver_index)

    # adapters
    if (database == 'MySQL'):
        pass
    else:
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('adapters')
        ut.create_folder('user')
        os.chdir('user')
        ut.create_folder('controllers')
        ut.create_folder('data-access')
        ut.create_folder('express-callback')
        os.chdir('controllers')
        ut.create_file('index.js', contents.adapters_user_controllers_index)
        ut.create_file('user-post.js', contents.adapters_user_controllers_post)
        os.chdir('..')
        os.chdir('data-access')
        ut.create_file('index.js', contents.adapters_user_data_access_index_mongo)
        ut.create_file('user-db.js', contents.adapters_user_data_access_user_db_mongo)
        os.chdir('..')
        os.chdir('express-callback')
        ut.create_file('index.js', contents.apdaters_user_express_callback)

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
    ut.create_folder('entitie')
    ut.create_folder('adapters')
    ut.create_folder('useCases')
