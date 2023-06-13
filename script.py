import os
import tkinter as tk 
from tkinter import filedialog

def create_folder(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

def create_file(caminho, conteudo):
    with open(caminho, 'w') as arquivo:
        arquivo.write(conteudo)

def create_hexagonal_structure(name_project, local):
    os.chdir(local)
    create_folder(name_project)
    os.chdir(name_project)
    os.system('npm init')
    os.system('npm install express dotenv mongodb debug')
    os.system('npm install -D jest eslint')
    os.system('git init')

    # folders source
    create_folder('src')
    create_folder('tests')
    create_folder('.vscode')

    # src
    os.chdir('src')
    create_folder('bin')
    create_folder('domain')
    create_folder('infrastructure')
    create_folder('interfaces')
    create_folder('useCases')

    # bin
    os.chdir('bin')
    create_file('www', '''
#!/usr/bin/env node

/**
 * Module dependencies.
 */

const debug = require('debug')('demo:server')
const http = require('http')
const app = require('../infrastructure/user/webserver')

/**
 * Normalize a port into a number, string, or false.
 */

function normalizePort (val) {
  const port = parseInt(val, 10)

  // eslint-disable-next-line no-restricted-globals
  if (isNaN(port)) {
    // named pipe
    return val
  }

  if (port >= 0) {
    // port number
    return port
  }

  return false
}

/**
 * Get port from environment and store in Express.
 */

const port = normalizePort(process.env.PORT || '3000')
app.set('port', port)

/**
 * Create HTTP server.
 */

const server = http.createServer(app)

/**
 * Event listener for HTTP server "error" event.
 */

function onError (error) {
  if (error.syscall !== 'listen') {
    throw error
  }

  const bind = typeof port === 'string'
    ? `Pipe ${port}`
    : `Port ${port}`

  // handle specific listen errors with friendly messages
  switch (error.code) {
    case 'EACCES':
      console.error(`${bind} requires elevated privileges`)
      process.exit(1)
      break
    case 'EADDRINUSE':
      console.error(`${bind} is already in use`)
      process.exit(1)
      break
    default:
      throw error
  }
}

/**
 * Event listener for HTTP server "listening" event.
 */

function onListening () {
  const addr = server.address()
  const bind = typeof addr === 'string'
    ? `pipe ${addr}`
    : `port ${addr.port}`
  debug(`Listening on ${bind}`)
}

/**
 * Listen on provided port, on all network interfaces.
 */

server.listen(port)
server.on('error', onError)
server.on('listening', onListening)

    ''')

    # domain
    os.chdir('..')
    os.chdir('domain')
    create_folder('user')
    os.chdir('user')
    create_file('index.js', '''
const buildMakeUser = require('./userDomain')
const userValidate = require('./userValidate')

const makeUser = buildMakeUser(userValidate)

module.exports = makeUser

''')
    create_file('userDomain.js', '''
const buildMakeUser = (userValidate) => ({
  userName,
  userSurname,
  userEmail,
  userDocumentNumber
} = {}) => {
  if (!userName || !userSurname || !userEmail || !userDocumentNumber) {
    return {
      message: 'all properties are mandatory',
      statusCode: 400
    }
  }

  if (!userValidate({ cpf: userDocumentNumber, email: userEmail })) {
    return {
      message: 'invalid Data',
      statusCode: 400
    }
  }

  return Object.freeze({
    getUserName: () => userName,
    getUserSurname: () => userSurname,
    getUserEmail: () => userEmail,
    getUserDocumentNumber: () => userDocumentNumber
  })
}

module.exports = buildMakeUser

    ''')
    create_file('userValidate.js', '''
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const cpfRegex = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/

function validateCPF (cpf) {
  return cpfRegex.test(cpf)
}

function validateEmail (email) {
  return emailRegex.test(email)
}

function validateUser ({ cpf, email }) {
  const documentNumberIsValid = validateCPF(cpf)
  const emailIsValid = validateEmail(email)
  return documentNumberIsValid && emailIsValid
}

module.exports = validateUser

    ''')
    # infrastructure
    os.chdir('..')
    os.chdir('..')
    os.chdir('infrastructure')
    create_folder('user')
    os.chdir('user')
    create_folder('db')
    create_folder('webserver')
    os.chdir('db')
    create_file('index.js', '''
const mongodb = require('mongodb')
require('dotenv').config()

const { MongoClient, ServerApiVersion } = mongodb
const url = process.env.USER_DB_URL
const dbName = process.env.USER_DB_NAME
const client = new MongoClient(url, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true
  }
})

const makeDb = async () => {
  await client.connect()
  console.log('Connected to database')
  return client.db(dbName)
}

module.exports = makeDb

    ''')
    os.chdir('..')
    os.chdir('webserver')
    create_file('routes.js', '''
const express = require('express')

const { userPost } = require('../../../interfaces/user/controllers')
const makeCallback = require('../../../interfaces/user/express-calback')

const router = express.Router()

router
  .post('/user', makeCallback(userPost))

module.exports = router

    ''')
    create_file('index.js', '''
const express = require('express')
const routes = require('./routes')

const app = express()

app.use(express.json())
app.use(routes)

module.exports = app

    ''')

    # interfaces
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    os.chdir('interfaces')
    create_folder('user')
    os.chdir('user')
    create_folder('controllers')
    create_folder('data-access')
    create_folder('express-callback')
    os.chdir('controllers')
    create_file('index.js', '''
const { createUser } = require('../../../useCases/user')
const makeUserPost = require('./user-post')

const userPost = makeUserPost({ createUser })

const userController = Object.freeze({
  userPost
})

module.exports = userController

    ''')
    create_file('user-post.js', '''
const makeUserPost = ({ createUser }) => async (httpRequest) => {
  try {
    const { source = {}, ...userInfo } = httpRequest.body
    source.ip = httpRequest.ip
    source.browser = httpRequest.headers['User-Agent']
    if (httpRequest.headers.Referer) {
      source.referrer = httpRequest.headers.Referer
    }
    const userCreatedOrError = await createUser({
      ...userInfo
    })

    if (userCreatedOrError.error) {
      return userCreatedOrError
    }

    return {
      headers: {
        'Content-Type': 'application/json',
        'Last-Modified': new Date(userCreatedOrError.modifieOn).toUTCString()
      },
      body: { userCreatedOrError }
    }
  } catch (error) {
    return {
      headers: {
        'Content-Type': 'application/json'
      },
      stausCode: 400,
      body: {
        error: error.message,
        codeError: 'COD1000X'
      }
    }
  }
}

module.exports = makeUserPost

    ''')
    os.chdir('..')
    os.chdir('data-access')
    create_file('index.js', '''
const makeUserDb = require('./user-db')
const makeDb = require('../../../infrastructure/user/db')

const userDb = makeUserDb({ makeDb })

module.exports = userDb

    ''')
    create_file('user-db.js', '''
const makeUserDb = ({ makeDb }) => {
  async function insert ({ ...userInfo }) {
    try {
      const db = await makeDb()

      const result = await db
        .collection('users')
        .insertOne(userInfo)

      const { ...insertedInfo } = result
      return { insertedInfo }
    } catch (error) {
      return {
        codeError: 'COD1002X',
        error
      }
    }
  }

  async function find ({ email }) {
    try {
      const db = await makeDb()

      const result = await db
        .collection('users')
        .findOne({ userEmail: email })

      return result
    } catch (error) {
      return {
        body: {
          codeError: 'COD1001X'
        },
        error
      }
    }
  }

  return Object.freeze({
    insert,
    find
  })
}

module.exports = makeUserDb

    ''')
    os.chdir('..')
    os.chdir('express-callback')
    create_file('index.js', '''
const makeExpressCallback = (controller) => async (req, res) => {
  const httpRequest = {
    body: req.body,
    query: req.query,
    params: req.params,
    ip: req.ip,
    method: req.method,
    path: req.path,
    headers: {
      'Content-Type': req.get('Content-Type'),
      Referer: req.get('referer'),
      'User-Agent': req.get('User-Agent')
    }
  }

  try {
    const httpResponse = await controller(httpRequest)

    if (httpResponse.headers) {
      res.set(httpResponse.headers)
    }

    res.type('json')
    res.status(httpResponse.body.userCreatedOrError.statusCode).send(httpResponse.body)
  } catch (error) {
    res.status(500).send({ error: 'An unknown error occurred.' })
  }
}

module.exports = makeExpressCallback

    ''')
    # useCases
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    os.chdir('useCases')
    create_folder('user')
    os.chdir('user')
    create_file('index.js', '''
const makeCreateUser = require('./createUser')
const userDb = require('../../interfaces/user/data-access')

const createUser = makeCreateUser({ userDb })

const userService = Object.freeze({
  createUser
})

module.exports = userService

    ''')
    create_file('createUser.js', '''
const makeUser = require('../../domain/user')

const createUser = ({ userDb }) => async (userInfo) => {
  const userOrError = makeUser(userInfo)

  if (userOrError.message) {
    return {
      message: userOrError.message,
      statusCode: userOrError.statusCode
    }
  }

  const user = userOrError
  const existingUser = await userDb.find({ email: user.getUserEmail() })

  if (!(existingUser)) {
    const userCreated = await userDb.insert({
      userName: user.getUserName(),
      userSurName: user.getUserSurname(),
      userEmail: user.getUserEmail(),
      userDocument: user.getUserDocumentNumber()
    })
    return {
      userCreated,
      statusCode: 201
    }
  }

  if (existingUser.body) {
    return {
      body: existingUser.body,
      statusCode: 500,
      error: existingUser.error
    }
  } else {
    return {
      message: 'User already exists',
      statusCode: 409
    }
  }
}

module.exports = createUser

    ''')

    # tests

    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    os.chdir('tests')
    create_folder('unit')
    os.chdir('unit')
    create_folder('domain')
    create_folder('interfaces')
    create_folder('useCases')


if __name__ == '__main__':
    print('CLI')
    name = str(input('nome do projeto: '))
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    create_hexagonal_structure(name, folder_path)
