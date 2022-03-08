;(function (backEndEnabled) {
    if (backEndEnabled && !XMLHttpRequest.prototype.sendAsBinary) {
        XMLHttpRequest.prototype.sendAsBinary = sendAsBinary;
    }

    var predictionThreshold = 0.60;
    var canvas = document.getElementById('show-image');
    var context = canvas.getContext('2d');

    //画布加载输出层默认图片
    drawImage("../static/images/out1.png");
    context.strokeStyle = "#f00";

    var modelName = 'Cnn2dCCPDD_dense96_filters192';
    var model = backEndEnabled ?
        'http://jsfzzx.gtis.com.cn/detection/troop/' + modelName :
        getModel('../kerasmodels', modelName);
    var xMaxSize = canvas.width, yMaxSize = canvas.height;

    //上传的内容
    var inputImageElement1 = document.getElementById('file1');
    var inputImageElement2 = document.getElementById('file2');
    //神经层图片
    var mediImgElement = document.getElementById('mediImg');

    //触发按钮
    var findExcavatorElement = document.getElementById('find-excavator');
    findExcavatorElement.onclick = findExcavators;

    function findExcavators() {
        document.getElementById("result_notice1").style.display = "none";
        document.getElementById("result_notice2").style.display = "none";

        //先判断是否有上传了图片
        var imgUrl1 = document.getElementById('imgUrl1').value;
        if (imgUrl1 == undefined || imgUrl1 == '') {
            document.getElementById("notice1").style.display = "";
            return;
        }

        var imgUrl2 = document.getElementById('imgUrl2').value;
        if (imgUrl2 == undefined || imgUrl2 == '') {
            document.getElementById("notice2").style.display = "";
            return;
        }

        if (imgUrl1 == imgUrl2) {
            setTimeout(function () {
                //没有识别到差异
                $(mediImgElement).attr({'src': '../static/images/medi3.png'});
                drawImage("../static/images/out4.png");
                document.getElementById("result_notice2").style.display = "";
            }, 1500);
        }

        //计算中，修改神经层和输出层图片
        $(mediImgElement).attr({'src': '../static/images/medi2.png'});
        drawImage("../static/images/out2.png");

        //
        findExcavatorsInBackEndTwice(new Date());
    }

    function sendAsBinary(datastr) {
        function byteValue(x) {
            return x.charCodeAt(0) & 0xff;
        }

        var ords = Array.prototype.map.call(datastr, byteValue);
        var ui8a = new Uint8Array(ords);
        this.send(ui8a.buffer);
    }

    function getModel(modelDir, modelName) {
        var modelPath = [modelDir, modelName].join('/');
        return new KerasJS.Model({
            filepaths: {
                model: modelPath + '.json',
                weights: modelPath + '_weights.buf',
                metadata: modelPath + '_metadata.json'
            }
        });
    }

    function drawImage(imageUrl) {
        var image = new Image();
        image.src = imageUrl;
        image.onload = function () {
            context.drawImage(image, 0, 0, xMaxSize, yMaxSize);
        };
    }

    function findExcavatorsInBackEndTwice(beginTime) {
        let firstGroupOfRanges = null;

        return post(inputImageElement1)
            .then(responseText => {
                firstGroupOfRanges = extractRanges(responseText);
                return post(inputImageElement2);
            })
            .then(responseText => {
                const secondGroupOfRanges = extractRanges(responseText);
                handleGroupsOfRanges(firstGroupOfRanges, secondGroupOfRanges, beginTime)
            })
            .catch(status => {
                alert('查询出错，错误代码：' + status);
            });
    }

    function post(fileInputElement) {
        return new Promise((resolve, reject) => {
            const formData = new FormData();
            formData.append('image', fileInputElement.files[0]);
            const xhr = new XMLHttpRequest();
            const url = model + '?threshold=' + predictionThreshold + '&shape=' + canvas.width + '&shape=' + canvas.height;
            xhr.open('POST', url, true);
            xhr.setRequestHeader("Accept", "application/json");

            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4) {
                    if (xhr.status === 200) {
                        resolve(xhr.responseText);
                    } else if (xhr.status >= 400) {
                        reject(xhr.status)
                    }
                }
            };
            xhr.send(formData);
        });
    }

    function extractRanges(responseText) {
        return JSON.parse(responseText).ranges;
    }

    function handleGroupsOfRanges(oldRanges, newRanges, beginTime) {
        //计算后，修改神经层
        $(mediImgElement).attr({'src': '../static/images/medi3.png'});

        //处理结果
        const emergedRanges = newRanges.filter(range => {
            return !hasAnyAlmostTheSameRange(range, oldRanges);
        });
        const disappearedRanges = oldRanges.filter(range => {
            return !hasAnyAlmostTheSameRange(range, newRanges);
        });
        const ranges = [];
        if (emergedRanges.length > 0) {
            ranges.push(emergedRanges[0]);
        }
        if (disappearedRanges.length > 0) {
            ranges.push(disappearedRanges[0]);
        }
        handleResultRanges(ranges, beginTime);
    }

    function handleResultRanges(ranges, beginTime) {
        if (ranges.length > 0) {
            drawRectangles(ranges, beginTime);

            //修改结果提示：识别出目标。
            document.getElementById("result_notice1").style.display = "";
        } else {
            //没有识别到差异
            drawImage("../static/images/out4.png");
            document.getElementById("result_notice2").style.display = "";
        }
    }

    function hasAnyAlmostTheSameRange(range, otherRanges) {
        const foundIndex = otherRanges.findIndex(otherRange => {
            return isAlmostTheSameRect(range, otherRange);
        });
        return foundIndex >= 0;
    }

    function isAlmostTheSameRect(rect_0, rect_1) {
        const AREA_RATIO_THRESH = 0.64;
        const area_0 = areaOfRect(rect_0);
        const area_1 = areaOfRect(rect_1);
        if (area_0 / area_1 < AREA_RATIO_THRESH || area_1 / area_0 < AREA_RATIO_THRESH) {
            return false;
        }

        const INTER_SIZE_THRESH = 3.0;
        const [xMin_0, yMin_0, xMax_0, yMax_0] = rect_0;
        const [xMin_1, yMin_1, xMax_1, yMax_1] = rect_1;
        const xMin_inter = Math.max(xMin_0, xMin_1);
        const xMax_inter = Math.min(xMax_0, xMax_1);
        const xInterSize = xMax_inter - xMin_inter;
        if (xInterSize < INTER_SIZE_THRESH) {
            return false;
        }
        const yMin_inter = Math.max(yMin_0, yMin_1);
        const yMax_inter = Math.min(yMax_0, yMax_1);
        const yInterSize = yMax_inter - yMin_inter;
        if (yInterSize < INTER_SIZE_THRESH) {
            return false;
        }

        const INTER_AREA_RATIO_PROD_THRESH = 0.64;
        const interArea = xInterSize * yInterSize;
        if ((interArea / area_0) * (interArea / area_1) < INTER_AREA_RATIO_PROD_THRESH) {
            return false
        }

        // Your are lucky here!
        return true;
    }

    function areaOfRect(rect) {
        return (rect[2] - rect[0]) * (rect[3] - rect[1]);
    }

    function drawRectangles(rectangles, beginTime) {
        const imageUrl = URL.createObjectURL(inputImageElement2.files.item(0));
        const image = new Image();
        image.src = imageUrl;
        image.onload = function () {
            //修改输出层图片
            context.drawImage(image, 0, 0, xMaxSize, yMaxSize);
            context.beginPath();
            rectangles.forEach(rect => drawRectangle(rect, context))
            context.stroke();
        };
        console.log('found in ' + (new Date().getTime() - beginTime.getTime()) + 'milliseconds.');
    }

    function drawRectangle(rect, context) {
        //挖掘机位置划线
        const xFrom = rect[0], yFrom = rect[1];
        const xTo = rect[2] - 1, yTo = rect[3] - 1;
        context.moveTo(xFrom, yFrom);
        context.lineTo(xTo, yFrom);
        context.lineTo(xTo, yTo);
        context.lineTo(xFrom, yTo);
        context.lineTo(xFrom, yFrom);
    }
})(!window.KerasJS);
