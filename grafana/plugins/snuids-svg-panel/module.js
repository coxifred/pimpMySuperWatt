/*! For license information please see module.js.LICENSE.txt */
define(["react","emotion","@grafana/ui","@grafana/data"],(function(e,t,n,a){return function(e){var t={};function n(a){if(t[a])return t[a].exports;var o=t[a]={i:a,l:!1,exports:{}};return e[a].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=e,n.c=t,n.d=function(e,t,a){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(n.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(a,o,function(t){return e[t]}.bind(null,o));return a},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/",n(n.s=4)}([function(t,n){t.exports=e},function(e,n){e.exports=t},function(e,t){e.exports=n},function(e,t){e.exports=a},function(e,t,n){"use strict";n.r(t);var a=n(3);function o(e,t){return Object.defineProperty?Object.defineProperty(e,"raw",{value:t}):e.raw=t,e}var i,r,l,s,d,u,c,p,h=n(0),f=n.n(h),m=n(1),g=n(2),b=Object(g.stylesFactory)((function(){return{wrapper:Object(m.css)(s||(s=o(["\n      position: relative;\n    "],["\n      position: relative;\n    "]))),svg:Object(m.css)(d||(d=o(["\n      position: absolute;\n      top: 0;\n      left: 0;\n    "],["\n      position: absolute;\n      top: 0;\n      left: 0;\n    "]))),textBox:Object(m.css)(u||(u=o(["\n      position: absolute;\n      bottom: 0;\n      left: 0;\n      padding: 10px;\n    "],["\n      position: absolute;\n      bottom: 0;\n      left: 0;\n      padding: 10px;\n    "]))),valueBox:Object(m.css)(c||(c=o(["\n      position: absolute;\n      top: 45%;\n      left: 0;\n      right: 0;\n      text-align: center;\n      padding: 0px;\n    "],["\n      position: absolute;\n      top: 45%;\n      left: 0;\n      right: 0;\n      text-align: center;\n      padding: 0px;\n    "]))),errorMessage:Object(m.css)(p||(p=o(["\n      position: absolute;\n      top: 0;\n      left: 0;\n      padding: 10px;\n      color: red;\n    "],["\n      position: absolute;\n      top: 0;\n      left: 0;\n      padding: 10px;\n      color: red;\n    "])))}}));n.d(t,"plugin",(function(){return v}));var v=new a.PanelPlugin((function(e){var t=e.options,n=e.data,a=e.width,s=e.height,d=Object(g.useTheme)(),u=b(),c=n.series.map((function(e){return e.fields.find((function(e){return"number"===e.type}))})).map((function(e){var t;return null===(t=e)||void 0===t?void 0:t.values.get(e.values.length-1)}))[0],p=c<=t.thresholdlow?t.lowcolor:c>t.thresholdhigh?t.highcolor:t.middlecolor,h=n.series.length<1?"No time series defined":n.series[0].fields.length<2?"No values defined":"";return f.a.createElement("div",{className:Object(m.cx)(u.wrapper,Object(m.css)(i||(i=o(["\n          width: ","px;\n          height: ","px;\n        "],["\n          width: ","px;\n          height: ","px;\n        "])),a,s))},f.a.createElement("div",{className:u.errorMessage},h),t.addLinks&&t.addLinks.length>0?f.a.createElement("a",{href:t.addLinks,target:t.openInNextTab?"_blank":"_self"},f.a.createElement("svg",{viewBox:t.viewbox,className:u.svg,width:a,height:s},f.a.createElement("g",{stroke:p,fill:p},f.a.createElement("path",{d:t.svg})))):f.a.createElement("svg",{viewBox:t.viewbox,className:u.svg,width:a,height:s},f.a.createElement("g",{stroke:p,fill:p},f.a.createElement("path",{d:t.svg}))),f.a.createElement("div",{className:u.valueBox},t.showSeriesValue&&t.addLinks&&t.addLinks.length>0&&f.a.createElement("div",{className:Object(m.css)(r||(r=o(["\n              font-size: ",";\n              color: ",";\n            "],["\n              font-size: ",";\n              color: ",";\n            "])),d.typography.size[t.seriesCountSize],t.valuecolor)},f.a.createElement("a",{href:t.addLinks,target:t.openInNextTab?"_blank":"_self"},c,t.units)),t.showSeriesValue&&0===t.addLinks.length&&f.a.createElement("div",{className:Object(m.css)(l||(l=o(["\n              font-size: ",";\n              color: ",";\n            "],["\n              font-size: ",";\n              color: ",";\n            "])),d.typography.size[t.seriesCountSize],t.valuecolor)},c,t.units)),f.a.createElement("div",{className:u.textBox},f.a.createElement("div",null,t.description)))})).setPanelOptions((function(e){return e.addTextInput({path:"svg",name:"SVG graphic",description:"The SVG graphic definition to use",defaultValue:"M462.3 62.6C407.5 15.9 326 24.3 275.7 76.2L256 96.5l-19.7-20.3C186.1 24.3 104.5 15.9 49.7 62.6c-62.8 53.6-66.1 149.8-9.9 207.9l193.5 199.8c12.5 12.9 32.8 12.9 45.3 0l193.5-199.8c56.3-58.1 53-154.3-9.8-207.9z"}).addTextInput({path:"viewbox",name:"View Box",description:"The view box size",defaultValue:"0 0 512 512"}).addColorPicker({path:"lowcolor",name:"Lower Color",description:"The color used when the data is below the threshold",defaultValue:"red"}).addColorPicker({path:"middlecolor",name:"Middle Color",description:"The color used when the data is between the threshold",defaultValue:"orange"}).addColorPicker({path:"highcolor",name:"High Color",description:"The color used when the data is above the threshold",defaultValue:"green"}).addNumberInput({path:"thresholdlow",name:"Threshold Minimum",description:"Value below that will be displayed with the lower color",defaultValue:0}).addNumberInput({path:"thresholdhigh",name:"Threshold Maximum",description:"Value above that will be displayed with the high color",defaultValue:100}).addTextInput({path:"description",name:"Description",description:"Description of the panel",defaultValue:"My beautiful panel"}).addTextInput({path:"addLinks",name:"Add Links",description:"Use $series_name to resolve series name in links",defaultValue:""}).addBooleanSwitch({path:"openInNextTab",name:"",description:"Open in next tab",defaultValue:!1}).addBooleanSwitch({path:"showSeriesValue",name:"Show series value",defaultValue:!1}).addRadio({path:"seriesCountSize",defaultValue:"sm",name:"Series counter size",settings:{options:[{value:"sm",label:"Small"},{value:"md",label:"Medium"},{value:"lg",label:"Large"}]},showIf:function(e){return e.showSeriesValue}}).addColorPicker({path:"valuecolor",name:"Value Color",description:"The color used to display the data",defaultValue:"grey",showIf:function(e){return e.showSeriesValue}}).addTextInput({path:"units",name:"Units",description:"The optional unit label",defaultValue:" MB"})}))}])}));
//# sourceMappingURL=module.js.map