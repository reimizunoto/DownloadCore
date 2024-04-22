
var _0xc6b4e6 = function(_0x1d70f8) {
    var _0x1020e5 = '';
    const _0x5af0f3 = 0x619;
    const _0x3218fa = _0x1d70f8['length'];
    for (var _0x14508c = 0x0; _0x14508c < _0x3218fa; _0x14508c += 0x2) {
        var _0x2b5229 = parseInt(_0x1d70f8[_0x14508c] + _0x1d70f8[_0x14508c + 0x1], 0x10);
        _0x2b5229 = ((((_0x2b5229 + 0x100000) - _0x5af0f3) - (((_0x3218fa / 0x2) - 0x1) - (_0x14508c / 0x2))) % 0x100);
        _0x1020e5 = String['fromCharCode'](_0x2b5229) + _0x1020e5;
    }
    _0x1d70f8 = _0x1020e5;
    return _0x1d70f8;
}

function setPlayFrm(playUrl) {
    let _0x17d66e = 'yh_playfram';
    var _0x1f18f3 = {
        'AasWO': function(_0x437b41, _0x3c4f14) {
            return _0x437b41 + _0x3c4f14;
        },
        'syElO': '/playurl?aid=$1&playindex=$2&epindex=$3',
        'xZmLE': '&r=',
        'fMeNX': function(_0x155206, _0x1216f2, _0x130c52, _0x439436) {
            return _0x155206(_0x1216f2, _0x130c52, _0x439436);
        }
    };
    const _0x2e5e87 = playUrl['replace'](/^.+?\/(\d+)-(\d+)-(\d+).*$/, _0x1f18f3['AasWO'](_0x1f18f3['syElO'] + _0x1f18f3['xZmLE'], Math['random']()));
    // _0x1f18f3['fMeNX'](playUrl, _0x17d66e, _0x2e5e87, 0x0);
    return _0x2e5e87
}

// $['get'](_0x5c7162, function(_0x5f0ee5, _0xf6f90) {
    
//     if (_0x5f0ee5['indexOf']('not\x20verified') >= 0x0) {
//         if (_0x6bcb0c < 0x3) {
//             return playUrl(_0x2d55c4, _0x5c7162, _0x6bcb0c + 0x1);
//         } else {
//             return ![];
//         }
//     }
//     if (ipchk_getplay(_0x5f0ee5)) {
//         return ![];
//     }
//     var _0x2e779f = _0xc6b4e6['purl'];
//     var _0x5cd6dc = _0xc6b4e6['vurl'];
//     var _0x41746d = _0xc6b4e6['inv'];
//     if (_0x5cd6dc && _0x41746d != '1') {
//         document['getElementById'](_0x2d55c4)['src'] = _0x2e779f + _0x5cd6dc;
//         return !![];
//     } else {
//         if (_0x6bcb0c < 0x3) {
//             setTimeout(function() {
            
//                 return playUrl(_0x2d55c4, _0x5c7162, _0x6bcb0c + 0x1);
//             }, 0xfa0);
//         } else {
//             document['getElementById'](_0x2d55c4)['src'] = _0x2e779f + _0x5cd6dc;
//         }
//     }
// });

// function ipchk_getplay(_0x2b5157) {
    
//     const _0x2be30a = _0x2b5157['match'](/^ipchk:(.+)/);
//     if (_0x2be30a) {
//         $('#ipchk_getplay')['html'](_0x2b5157);
//         $('#ipchk_getplay')['removeAttr']('hidden');
//         return !![];
//     }
//     return ![];
// }
function GetUrlQuery(in_url){
    in_query = 'url';
    var reg = new RegExp("[?&]+"+in_query+"=([^&]*)");
    var re_resl = in_url.match(reg);
    if(re_resl){
        var qVal = re_resl[1];
        if(qVal){
            qVal = qVal.replace(/[+]{1}/g, " ");
            qVal = decodeURIComponent(qVal);
            return qVal;
        }
    }
    return null;
}
console.log(GetUrlQuery('https://www.iyhdmm.com/tpsf/player/dpx2/?hls=1&url=https%3A%2F%2Fs10.fsvod1.com%2F20240302%2Fg4t0A5MD%2Findex.m3u8'));