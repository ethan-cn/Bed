var dom = document.getElementById('clock');
var ctx = dom.getContext('2d');
var width = ctx.canvas.width;
var height = ctx.canvas.height;
var r = width / 2;
//定义钟盘
function drawBackground(){
    ctx.save();
    ctx.translate(r, r);
    ctx.beginPath();
    ctx.lineWidth = 10;
    ctx.font ='18px Arial';
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.arc(0, 0, r-5, 0, 2 * Math.PI, false);
    ctx.stroke();
    var hourNumbers = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2];
    //遍历获取坐标
    hourNumbers.forEach(function(number, i){
        var rad = 2 * Math.PI / 12 * i;
        var x = Math.cos(rad) * (r - 30);
        var y = Math.sin(rad) * (r - 30);
        ctx.fillText(number, x ,y);
    })

    //定义刻度
    for(var i=0;i<60;i++){
        var rad = 2 * Math.PI / 60 * i;
        var x = Math.cos(rad) * (r - 18);
        var y = Math.sin(rad) * (r - 18);
        ctx.beginPath();
        if(i % 5 == 0){
            ctx.arc(x, y, 2, 0, 2 * Math.PI, false);
            ctx.fillStyle = '#000';
        }else{
            ctx.arc(x, y, 2, 0, 2 * Math.PI, false);
            ctx.fillStyle = '#ccc';
        }
        ctx.fill();
    }

}

//定义时钟
function drawHour(hour,minute){
    ctx.save();
    ctx.beginPath();
    var rad = 2 * Math.PI / 12 * hour;
    var mrad = 2 * Math.PI / 12 / 60 * minute;
    ctx.rotate(rad + mrad);
    ctx.lineWidth = 6;
    ctx.lineCap= 'round';
    ctx.moveTo(0 ,10);
    ctx.lineTo(0 ,-r / 2);
    ctx.stroke();
    ctx.restore();
}
//定义分钟
function drawMinute(minute,second){
    ctx.save();
    ctx.beginPath();
    var rad = 2 * Math.PI / 60 * minute;
    var srad = 2 * Math.PI / 60 /60 * second;
    ctx.rotate(rad + srad);
    ctx.lineWidth = 3;
    ctx.lineCap= 'round';
    ctx.moveTo(0 ,10);
    ctx.lineTo(0 ,-r + 18);
    ctx.stroke();
    ctx.restore();
}
//定义秒钟
function drawSecond(second){
    ctx.save();
    ctx.beginPath();
    var rad = 2 * Math.PI / 60 * second;
    ctx.rotate(rad);
    ctx.lineWidth = 3;
    ctx.lineCap= 'round';
    ctx.moveTo(-2 ,20);
    ctx.lineTo( 2, 20);
    ctx.lineTo( 1, -r + 18);
    ctx.lineTo( -1, -r + 18);
    ctx.fillStyle = '#c14543';
    ctx.fill();
    ctx.restore();
}
//定义钟盘圆点样式
function drawDot(){
    ctx.beginPath();
    ctx.fillStyle = '#fff';
    ctx.arc(0, 0, 3, 0, 2 * Math.PI, false);
    ctx.fill();
}

//时间函数
function draw(){
    ctx.clearRect(0, 0, width, height);
    var now = new Date();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
    drawBackground();
    drawHour(hour,minute);
    drawMinute(minute,second);
    drawSecond(second);
    drawDot();
    ctx.restore();
}
setInterval(draw, 1000);