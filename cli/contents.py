www  = '''#!/usr/bin/env node

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
'''

user_entitie_index = '''const buildMakeUser = require('./userEntitie')
const userValidate = require('./userValidate')

const makeUser = buildMakeUser(userValidate)

module.exports = makeUser
'''

user_entitie = '''const buildMakeUser = (userValidate) => ({
  userName,
  userSurname,
  userEmail,
  userDocumentNumber
} = {}) => {
  if (!userName || !userSurname || !userEmail || !userDocumentNumber) {
    return {
      error: {
        message: 'all properties are mandatory',
        statusCode: 400
      }
    }
  }

  if (!userValidate({ cpf: userDocumentNumber, email: userEmail })) {
    return {
      error: {
        message: 'invalid Data',
        statusCode: 400
      }
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
'''

entitie_user_validate = '''const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
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
'''

infrastructure_user_db_mysql = ''''const mysql = require('mysql2')
require('dotenv').config()

const host = process.env.MY_SQL_HOST
const user = process.env.MY_SQL_USER
const password = process.env.MY_SQL_PASS
const database = process.env.MY_SQL_DATABASE

const connection = mysql.createConnection({
  host,
  user,
  password,
  database
})

module.exports = connection
'''

infrastructure_user_db_mongo = '''const mongodb = require('mongodb')
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
'''

infrastructure_user_webserver_routes =  '''const express = require('express')

const { userPost } = require('../../../adapters/user/controllers')
const makeCallback = require('../../../adapters/user/express-callback')

const router = express.Router()

router
  .post('/user', makeCallback(userPost))

module.exports = router
'''

infrastructure_user_webserver_index = '''const express = require('express')
const routes = require('./routes')

const app = express()

app.use(express.json())
app.use(routes)

module.exports = app
'''

adapters_user_controllers_index = '''const { createUser } = require('../../../useCases/user')
const makeUserPost = require('./user-post')

const userPost = makeUserPost({ createUser })

const userController = Object.freeze({
  userPost
})

module.exports = userController
'''

adapters_user_controllers_post = '''const makeUserPost = ({ createUser }) => async (httpRequest) => {
  try {
    const { source = {}, ...userInfo } = httpRequest.body
    source.ip = httpRequest.ip
    source.browser = httpRequest.headers['User-Agent']
    
    const userCreatedOrError = await createUser({
      ...userInfo
    })

    if (userCreatedOrError.result instanceof Error) {
      return userCreatedOrError
    }

    if (userCreatedOrError.error) {
      return userCreatedOrError.error
    }

    return {
      headers: {
        'Content-Type': 'application/json',
        'Last-Modified': new Date(userCreatedOrError.modifieOn).toUTCString()
      },
      body: userCreatedOrError
    }
  } catch (error) {
    return {
      headers: {
        'Content-Type': 'application/json'
      },
      stausCode: 400,
      body: {
        error: error.message,
      }
    }
  }
}

module.exports = makeUserPost
'''

adapters_user_data_access_index_mongo = '''const makeUserDb = require('./user-db')
const makeDb = require('../../../infrastructure/user/db')

const userDb = makeUserDb({ makeDb })

module.exports = userDb
'''

adapters_user_data_access_user_db_mongo = '''const DatabaseError = require('../../../utils/databaseError')

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
      return new DatabaseError('Error in Adapter layer: Database Error', 'DB_ERROR', error)
    }
  }

  async function findOne({ email }) {
    try {
      const db = await makeDb()

      const result = await db
        .collection('users')
        .findOne({ userEmail: email })

      return result
    } catch (error) {
      return new DatabaseError('Error in Adapter layer: Database Error', 'DB_ERROR', error)
    }
  }

  async function find() {
    try {
      const db = await makeDb()
      
      const results = await db
        .collection('users')
        .find().toArray()
     
      return results
    } catch (error) {
      return new DatabaseError('Error in Adapter layer: DataBaseError', 'DB_ERROR', error)
    }
  }

  return Object.freeze({
    insert,
    findOne,
    find
  })
}

module.exports = makeUserDb
'''

apdaters_user_express_callback = '''const makeExpressCallback = (controller) => (req, res) => {
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
      'User-Agent': req.get('User-Agent'),
    },
  };
  controller(httpRequest)
    .then((httpResponse) => {
      if (httpResponse.headers) {
        res.set(httpResponse.headers);
      }
      res.type('json');
      res
        .status(httpResponse.statusCode || httpResponse.body.statusCode)
        .send(httpResponse.body || httpResponse);
    })
    .catch(() => res.status(500).send({ error: 'An unkown error occurred.' }));
};

module.exports = makeExpressCallback;
'''

use_cases_user_index = '''const makeCreateUser = require('./createUser')
const userDb = require('../../adapters/user/data-access')

const createUser = makeCreateUser({ userDb })

const userService = Object.freeze({
  createUser
})

module.exports = userService
'''

use_cases_user_create = '''const makeUser = require('../../entitie/user')
const DatabaseError = require('../../utils/databaseError')

const createUser = ({ userDb }) => async (userInfo) => {
  const userOrError = makeUser(userInfo)

  if (userOrError.error) {
    return {
      message: userOrError.error.message,
      statusCode: userOrError.error.statusCode
    }
  }

  const user = userOrError
  const result = await userDb.findOne({ email: user.getUserEmail() })

  if (!(result)) {
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

  if (result instanceof DatabaseError) {
    return {
      result,
      statusCode: 500,
    }
  } else {
    return {
      error: {
        message: 'User already exists',
        statusCode: 409
      }
    }
  }
}

module.exports = createUser
'''

gitignore = '''# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
.pnpm-debug.log*

# Diagnostic reports (https://nodejs.org/api/report.html)
report.[0-9]*.[0-9]*.[0-9]*.[0-9]*.json

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Directory for instrumented libs generated by jscoverage/JSCover
lib-cov

# Coverage directory used by tools like istanbul
coverage
*.lcov

# nyc test coverage
.nyc_output

# Grunt intermediate storage (https://gruntjs.com/creating-plugins#storing-task-files)
.grunt

# Bower dependency directory (https://bower.io/)
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons (https://nodejs.org/api/addons.html)
build/Release

# Dependency directories
node_modules/
jspm_packages/

# Snowpack dependency directory (https://snowpack.dev/)
web_modules/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Optional stylelint cache
.stylelintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variable files
.env
.env.development.local
.env.test.local
.env.production.local
.env.local

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Next.js build output
.next
out

# Nuxt.js build / generate output
.nuxt
dist

# Gatsby files
.cache/
# Comment in the public line in if your project uses Gatsby and not Next.js
# https://nextjs.org/blog/next-9-1#public-directory-support
# public

# vuepress build output
.vuepress/dist

# vuepress v2.x temp and cache directory
.temp
.cache

# Docusaurus cache and generated files
.docusaurus

# Serverless directories
.serverless/

# FuseBox cache
.fusebox/

# DynamoDB Local files
.dynamodb/

# TernJS port file
.tern-port

# Stores VSCode versions used for testing VSCode extensions
.vscode-test

# yarn v2
.yarn/cache
.yarn/unplugged
.yarn/build-state.yml
.yarn/install-state.gz
.pnp.*'''

util_database_error = '''class DatabaseError extends Error {
  constructor(message, code, error) {
    super(message)
    this.name = 'DatabaseError'
    this.code = code
    this.error = error
  }
}

module.exports = DatabaseError
'''