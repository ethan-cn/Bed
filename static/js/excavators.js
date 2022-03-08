;(function (backEndEnabled) {
    if (backEndEnabled && !XMLHttpRequest.prototype.sendAsBinary) {
        XMLHttpRequest.prototype.sendAsBinary = sendAsBinary;
    }

    var predictionThreshold = 0.60;
    var clipRangeScale = 2;
    var xStepRatio = 1 / 2, yStepRatio = 1 / 2;
    var canvas = document.getElementById('show-image');
    var context = canvas.getContext('2d');
    
    //画布加载输出层默认图片
    console.log('error')
    drawImage("../static/images/out1.png");
    context.strokeStyle = "#f00";
    
    var modelName = 'Cnn2dCCPDD_dense96_filters192';
     var model = backEndEnabled ?
         'http://jsfzzx.gtis.com.cn/detection/troop/' + modelName:
         getModel('../kerasmodels', modelName);
    var xMaxSize = canvas.width, yMaxSize = canvas.height;
    
    //上传的内容
    var inputImageElement = document.getElementById('file');
    //神经层图片
    var mediImgElement = document.getElementById('mediImg');
    
    //触发按钮
    var findExcavatorElement = document.getElementById('find-excavator');
    findExcavatorElement.onclick = findExcavators;
    function findExcavators () {
    	document.getElementById("result_notice1").style.display="none";
        document.getElementById("result_notice2").style.display="none";
    	
    	//先判断是否有上传了图片
    	var imgUrl = document.getElementById('imgUrl').value;
    	if(imgUrl == undefined || imgUrl == ''){
    		document.getElementById("notice").style.display="";
			return;
    	}
    	
    	//计算中，修改神经层和输出层图片
    	$(mediImgElement).attr({'src': "../static/images/medi2.png"});
    	drawImage("../static/images/out2.png");
    	
        var beginTime = new Date();
        if (backEndEnabled) {
            findExcavatorsInBackEnd(beginTime);
        } else {
            findExcavatorsInFrontEnd(beginTime);
        }
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

    function getClipShapes(xMinSize, yMinSize, xMaxSize, yMaxSize, scale) {
        var clipShapes = [];
        for (var xClipSize = xMinSize, yClipSize = yMinSize;
             xClipSize <= xMaxSize || yClipSize <= yMaxSize;
             xClipSize *= scale, yClipSize *= scale) {
            clipShapes.unshift([
                Math.floor(Math.min(xClipSize, xMaxSize)),
                Math.floor(Math.min(yClipSize, yMaxSize))
            ]);
        }
        clipShapes.unshift([xMaxSize, yMaxSize]);
        return clipShapes;
    }

    function drawImage(imageUrl) {
        var image = new Image();
        image.src = imageUrl;
        image.onload = function () {
            context.drawImage(image, 0, 0, xMaxSize, yMaxSize);
        };
    }

    function findExcavatorsInFrontEnd(beginTime) {
        if (model == null) return;
        var inputShape = model.inputTensors.input.tensor.shape;
        var xMinSize = inputShape[1], yMinSize = inputShape[0];
        var clipShapes = getClipShapes(xMinSize, yMinSize, xMaxSize, yMaxSize, clipRangeScale);
        var pixels = context.getImageData(0, 0, xMaxSize, yMaxSize).data;
        var pixelsSize = pixels.length;
        var bSourceSize = pixelsSize / xMaxSize / yMaxSize;
        var bTargetSize = 3;
        var clipShapesSize = clipShapes.length;

        var sourceFloatArray = new Float32Array(pixelsSize);
        for (var i = 0; i < pixelsSize; i++) {
            sourceFloatArray[i] = pixels[i] / 255;
        }

        var promise = null;
        for (var iSize = 0; iSize < clipShapesSize; iSize++) {
            var clipShape = clipShapes[iSize];
            var xClipSize = clipShape[0];
            var yClipSize = clipShape[1];
            var xStep = Math.floor(xClipSize * xStepRatio);
            var yStep = Math.floor(yClipSize * yStepRatio);
            for (var xBegin = 0, xEnd = xBegin + xClipSize; xEnd <= xMaxSize; xBegin += xStep, xEnd += xStep) {
                for (var yBegin = 0, yEnd = yBegin + yClipSize; yEnd <= yMaxSize; yBegin += yStep, yEnd += yStep) {
                    var clipRange = [xBegin, yBegin, xEnd, yEnd];
                    var targetFloatArray = reshape2dArray(sourceFloatArray, [xMaxSize, yMaxSize, bSourceSize],
                        [xMinSize, yMinSize, bTargetSize], clipRange);
                    promise = predictByModel(targetFloatArray, promise, drawRectangle.bind(null, clipRange, beginTime));
                }
            }
        }
    }

    function findExcavatorsInBackEnd(beginTime) {
        var formData = new FormData();
        formData.append('image', inputImageElement.files[0]);
//        formData.append('image', file);

        var xhr = new XMLHttpRequest();
        var url = model + '?threshold=' + predictionThreshold + '&shape=' + canvas.width + '&shape=' + canvas.height;
        xhr.open('POST', url, true);
        xhr.setRequestHeader("Accept", "application/json");

        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status === 200) {
                	//计算后，修改神经层
                	$(mediImgElement).attr({'src': "../static/images/medi3.png"});
                	
                    var ranges = JSON.parse(xhr.responseText).ranges;
                    if (ranges.length > 0) {
                        drawRectangle(ranges[0], beginTime);
                        //修改结果提示：识别出目标。
                        document.getElementById("result_notice1").style.display="";
                    } else {
                    	//没有识别到挖掘机
                    	drawImage("../static/images/out3.png");
                    	document.getElementById("result_notice2").style.display="";
                    }
                } else if (xhr.status >= 400) {
                    alert('查询出错，错误代码：' + xhr.status);
                }
            }
        };
        xhr.send(formData);
    }

    function reshape2dArray(sourceFloatArray, sourceShape, targetShape, clipRange) {
        var xSourceSize = sourceShape[0], ySourceSize = sourceShape[1], bSourceSize = sourceShape[2];
        var xTargetSize = targetShape[0], yTargetSize = targetShape[1], bTargetSize = targetShape[2];
        var xClipBegin = clipRange[0], yClipBegin = clipRange[1], xClipEnd = clipRange[2], yClipEnd = clipRange[3];
        var targetFloatArray = new Float32Array(xTargetSize * yTargetSize * bTargetSize);
        var xFactor = xTargetSize / (xClipEnd - xClipBegin), yFactor = yTargetSize / (yClipEnd - yClipBegin);
        for (var yTargetIndex = 0; yTargetIndex < yTargetSize; yTargetIndex++) {
            var ySourceIndex = Math.floor(yTargetIndex / yFactor + yClipBegin);
            for (var xTargetIndex = 0; xTargetIndex < xTargetSize; xTargetIndex++) {
                var xSourceIndex = Math.floor(xTargetIndex / xFactor + xClipBegin);
                var sourcePixelBeginIndex = (xSourceIndex + ySourceIndex * xSourceSize) * bSourceSize;
                var targetPixelBeginIndex = (xTargetIndex + yTargetIndex * xTargetSize) * bTargetSize;
                if (bSourceSize === bTargetSize || bSourceSize - bTargetSize === 1) {
                    var subArray = sourceFloatArray.subarray(sourcePixelBeginIndex, sourcePixelBeginIndex + bTargetSize);
                    targetFloatArray.set(subArray, targetPixelBeginIndex);
                } else {
                    // todo: 合并或拆分波段，或其他
                }
            }
        }
        return targetFloatArray;
    }

    function predictByModel(inputFloatArray, prevPromise, onPredictTrue) {
        var currentPromise = null;
        if (prevPromise == null) {
            currentPromise = pridict(inputFloatArray, onPredictTrue);
        } else {
            currentPromise = prevPromise.then(function () {
                return prevPromise.then(pridict.bind(window, inputFloatArray, onPredictTrue));
            })
        }
        return currentPromise;
    }

    function pridict(inputFloatArray, onPredictTrue) {
        var currentPromise = model.predict({'input': inputFloatArray});

        return currentPromise.then(function (result) {
            var output = result.output ? result.output[1] : -1;
            if (output > predictionThreshold) {
                console.log(output);
                onPredictTrue();
                throw 'found';
            } else {
                console.log(false);
            }
            return currentPromise;
        });
    }

    function drawRectangle(clipRange, beginTime) {
    	var imageUrl = URL.createObjectURL(inputImageElement.files.item(0));
        var image = new Image();
        image.src = imageUrl;
        image.onload = function () {
        	//修改输出层图片
            context.drawImage(image, 0, 0, xMaxSize, yMaxSize);
            //挖掘机位置划线
            var xFrom = clipRange[0], yFrom = clipRange[1];
	        var xTo = clipRange[2] - 1, yTo = clipRange[3] - 1;
	        context.beginPath();
	        context.moveTo(xFrom, yFrom);
	        context.lineTo(xTo, yFrom);
	        context.lineTo(xTo, yTo);
	        context.lineTo(xFrom, yTo);
	        context.lineTo(xFrom, yFrom);
	        context.stroke();
        };
        
        console.log('found in ' + (new Date().getTime() - beginTime.getTime()) + 'milliseconds.')
    }
})(!window.KerasJS);
