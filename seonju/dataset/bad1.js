const { exec } = require('child_process');
const express = require('express');
const app = express();
app.get('/readfile', (req, res) => {
  const filename = req.query.filename;
  exec(cat ${filename}, (error, stdout, stderr) => {
    if (error) {
      res.status(500).send(Error: ${stderr});
      return;
    }
    res.send(stdout);
  });
});
app.listen(3000, () => {
  console.log('Server running on port 3000');
});
