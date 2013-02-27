function myrect(ctx, x, y, w, h, s) {
  // bg
  ctx.strokeStyle = "blue";
  ctx.fillStyle = "lightgrey";
  ctx.fillRect(x, y, w, h);
  // margin
  ctx.strokeRect(x, y, w, h);
  // label
  ctx.textBaseline="top";
  ctx.textAlign="center";
  ctx.fillStyle = "black";
  ctx.fillText(s, x + w/2, y);
}

function main_loaded() {
  //console.log('tratata');
  var bodysize = document.getElementsByTagName("body")[0].getBoundingClientRect();
  var canvas=document.getElementById("canvas");
  var canvasize = canvas.getBoundingClientRect();
  cw = bodysize.right - canvasize.left - 5;
  ch = bodysize.bottom - canvasize.top - 8;
  canvas.width = cw;
  canvas.height = ch;
  var ctx = canvas.getContext('2d');
  // lets go
  var hw = 64;
  var hh = 32;
  var dow = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];
  // 1. background
  // 1.1. bg
  ctx.fillStyle = "silver";
  ctx.fillRect(0, 0, cw, ch);   // x, y, w, h
  ctx.font="12pt Arial";
  ctx.fillStyle = "black";
  ctx.strokeStyle = "yellow";
  ctx.moveTo(0, 0);
  ctx.lineTo(hw, hh);
  ctx.textBaseline="top";
  ctx.textAlign="right";
  ctx.fillText("Ч", hw, 0);
  ctx.textBaseline="bottom";
  ctx.textAlign="left";
  ctx.fillText("Д", 0, hh);
  // 1.2. table
  // 1.2.1. horizontal
  ctx.textBaseline="top";
  ctx.textAlign="left";
  dy = (ch - hh) / 7;
  for (i=0; i<7; i++) {
    y = hh + dy * i;
    ctx.moveTo(0, y);
    ctx.lineTo(cw, y);
    ctx.fillText(dow[i], 0, y);
  }
  // 1.2.2. vertical
  dx = (cw - hw) / 13;
  for (i=0; i<13; i++) {
    x = hw + dx * i;
    ctx.moveTo(x, 0);
    ctx.lineTo(x, ch);
    ctx.fillText((i + 8)+":00", x, 0);
  }  // 1.2.3. draw
  ctx.stroke();
  // 2. data
  myrect(ctx, hw + 2.0 * dx, hh + 1.00 * dy, dx * 2.50, dy, "Стоматолог");
  myrect(ctx, hw + 4.5 * dx, hh + 1.00 * dy, dx * 2.75, dy, "Окулист");
  myrect(ctx, hw + 4.5 * dx, hh + 1.50 * dy, dx * 1.50, dy/2, "Шишкин");
  myrect(ctx, hw + 6.0 * dx, hh + 1.50 * dy, dx * 1.25, dy/2, "Пышкиндт");
}
