const https = require('https');
const fs = require('fs');
const express = require('express');
const path = require('path');

const app = express();

// Путь к вашему SSL сертификату и ключу
const privateKey = fs.readFileSync('private.key', 'utf8');
const certificate = fs.readFileSync('certificate.crt', 'utf8');

// Настройка SSL-сертификатов
const credentials = { key: privateKey, cert: certificate};

// Указание, где находятся статические файлы (например, ваш HTML, CSS и JavaScript)
app.use(express.static(path.join(__dirname, 'public')));

// Роут для главной страницы
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Создание HTTPS сервера
https.createServer(credentials, app).listen(8080, () => {
  console.log('HTTPS сервер запущен на https://localhost:8080');
});
