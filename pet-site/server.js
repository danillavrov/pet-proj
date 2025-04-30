const express = require('express');
const path = require('path');

const app = express();

// Указание, где находятся статические файлы
app.use(express.static(path.join(__dirname, 'public')));

// Роут для главной страницы
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = 8080;
const HOST = '0.0.0.0';

app.listen(PORT, HOST, () => {
  console.log(`Сервер запущен на http://${HOST}:${PORT}`);
});