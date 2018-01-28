var proc = require('child_process');
var express = require('express');
var app 	= express();
var router 	= express.Router();
var bodyParser = require('body-parser');

const API_ROOT = "/validation"
const API_PORT = 8080

const COMMAND = "python validation_driver.py "

router.post('/', function(req, res){
    res.send('OKKKKKK')
	//var data = req.body
	//var doc = JSON.stringify(data.doc)
	//var base = JSON.stringify(data.base)
	//var regras = JSON.stringify(data.regras)
	//var args = doc + ' ' + base + ' ' + regras
	//var out = proc.execSync(COMMAND + args).toString('utf8')
	//res.send(out)
});

app.use(bodyParser.urlencoded({extended: true}))
app.use(bodyParser.json());
app.use(API_ROOT,router);
app.listen(API_PORT);
