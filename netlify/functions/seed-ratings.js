const admin = require('firebase-admin');

if (!admin.apps.length) {
  const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: 'https://hailoffire-campaign-default-rtdb.firebaseio.com'
  });
}

const db = admin.database();

// Seeded Elo ratings computed from team stats.
// Stored for each quality tier — quality differences emerge from real votes.
const SEEDED = {
  'de-td-jagdtiger':            1550,
  'de-spa-hummel':              1484,
  'de-spa-grille':              1468,
  'sv-tank-is2':                1461,
  'br-gun-55in':                1455,
  'us-spa-m12':                 1454,
  'de-gun-150mm-sfh18':         1454,
  'sv-tank-ot34':               1444,
  'br-tank-churchill-croc':     1438,
  'sv-spg-isu122':              1432,
  'de-td-jagdpanther':          1419,
  'us-tank-m26-pershing':       1395,
  'br-tank-challenger':         1388,
  'sv-spg-isu152':              1387,
  'de-tank-tiger2':             1386,
  'de-tank-tiger1':             1381,
  'us-tank-m4a3e8':             1377,
  'de-tank-panther':            1377,
  'de-tank-brummbar':           1376,
  'de-td-elefant':              1373,
  'sv-spg-su152':               1363,
  'sv-tank-kv8s':               1355,
  'de-gun-150mm-sig':           1353,
  'us-gun-155mm-howitzer':      1348,
  'br-spa-priest':              1346,
  'us-tank-m4a3e2-jumbo':       1341,
  'de-tank-stuh42':             1339,
  'br-tank-cromwell4':          1338,
  'us-spg-105mm-sherman':       1337,
  'sv-tank-t34-41':             1337,
  'br-tank-churchill7':         1332,
  'br-gun-25pdr':               1331,
  'sv-tank-t34-85':             1326,
  'br-tank-firefly':            1321,
  'us-td-m36':                  1318,
  'sv-gun-152mm-howitzer':      1318,
  'us-spa-m7-priest':           1317,
  'de-spa-wespe':               1317,
  'us-tank-m24-chaffee':        1314,
  'de-td-hornisse':             1313,
  'de-tank-pz4h':               1303,
  'br-spa-sexton':              1302,
  'sv-tank-kv1s':               1302,
  'br-td-m10c':                 1297,
  'sv-tank-kv85':               1297,
  'sv-spg-su122':               1293,
  'de-tank-stug':               1288,
  'de-td-jagdpanzer4':          1288,
  'br-tank-churchill6':         1288,
  'us-gun-105mm-howitzer':      1287,
  'de-gun-105mm-lefh18':        1287,
  'br-tank-cromwell6cs':        1284,
  'de-gun-pak43':               1283,
  'us-tank-m4-sherman-76':      1282,
  'us-tank-m4-sherman':         1279,
  'br-tank-sherman':            1279,
  'br-td-m10':                  1279,
  'de-gun-88mm-flak':           1278,
  'br-gun-37in-aa':             1277,
  'de-gun-75mm-gebg36':         1275,
  'sv-spg-su85':                1274,
  'sv-gun-zis2':                1272,
  'de-gun-pak40':               1265,
  'br-tank-churchill34':        1265,
  'us-td-m18-hellcat':          1259,
  'de-gun-88mm-launcher':       1256,
  'de-inf-panzerschreck':       1255,
  'us-td-m10':                  1250,
  'de-tank-pz3n':               1249,
  'sv-gun-zis3':                1246,
  'us-spg-m8-scott':            1243,
  'us-tank-m5-stuart':          1231,
  'br-tank-stuart':             1231,
  'sv-spg-su76m':               1226,
  'sv-gun-85mm-aa':             1223,
  'de-gun-75mm-leig':           1222,
  'de-gun-pak38':               1218,
  'br-gun-6pdr':                1218,
  'us-gun-105mm-light':         1215,
  'de-td-marder':               1205,
  'sv-gun-122mm-howitzer':      1205,
  'de-tank-pz3m':               1203,
  'us-inf-bazooka':             1202,
  'br-inf-piat':                1202,
  'br-gun-17pdr':               1194,
  'de-transport-sdkfz251-75cm': 1181,
  'us-gun-3in':                 1176,
  'br-ac-aec3':                 1173,
  'br-recon-universal-carrier-piat': 1173,
  'de-ac-puma':                 1172,
  'sv-tank-t70':                1172,
  'br-gun-75mm-pack':           1169,
  'us-gun-57mm':                1165,
  'br-gun-2pdr':                1165,
  'sv-gun-45mm':                1165,
  'br-spaa-bofors-sp':          1159,
  'de-gun-2cm-flak':            1158,
  'de-spaa-wirbelwind':         1157,
  'de-spa-sdkfz251-75cm':       1151,
  'de-ft-flammpanzer3':         1146,
  'de-gun-12cm-mortar':         1144,
  'de-spaa-sdkfz7':             1143,
  'br-gun-42in-mortar':         1143,
  'us-spaa-m15-cgmc':           1137,
  'de-spaa-sdkfz251-15mm':      1129,
  'us-ac-m8':                   1128,
  'de-spaa-sdkfz10':            1128,
  'de-spaa-sdkfz251-2cm':       1128,
  'br-ac-daimler1':             1128,
  'br-ac-humber4':              1128,
  'de-ac-sdkfz231':             1125,
  'sv-gun-120mm-mortar':        1113,
  'us-gun-37mm':                1112,
  'de-spa-panzerwerfer':        1089,
  'us-gun-81mm-mortar':         1081,
  'de-gun-8cm-mortar':          1081,
  'de-ac-sdkfz222':             1081,
  'de-ac-sdkfz250':             1081,
  'br-gun-3in-mortar':          1081,
  'br-ac-humber23':             1081,
  'us-gun-bofors':              1078,
  'de-ft-sdkfz251-flame':       1078,
  'sv-ac-ba64':                 1074,
  'br-gun-bofors-40mm':         1070,
  'sv-gun-37mm-aa':             1070,
  'br-ac-aec1':                 1054,
  'sv-gun-82mm-mortar':         1052,
  'sv-gun-ptrd':                1050,
  'us-gun-quad-50cal-aa':       1048,
  'br-inf-2in-mortar':          1046,
  'us-gun-50cal-aa':            1042,
  'us-spa-m4-81mm':             1033,
  'br-recon-universal-carrier-mg':   1028,
  'br-recon-universal-carrier-boys': 1021,
  'br-recon-humber-lrc':        1021,
  'br-recon-otter-lrc':         1021,
  'us-spaa-m16-mgmc':           1019,
  'us-gun-60mm-mortar':         1016,
  'us-gun-hmg':                 1013,
  'de-gun-hmg':                 1013,
  'br-gun-vickers':             1013,
  'sv-gun-maksim':              1013,
  'sv-spaa-zsu-m17':            1013,
  'us-spaa-m13-mgmc':           1011,
  'us-inf-mg':                  1004,
  'de-inf-mg':                  1004,
  'de-spa-sdkfz251-8cm':        1004,
  'br-inf-mg':                  1004,
  'sv-inf-smg':                 1002,
  'us-inf-rifle-mg':             997,
  'de-inf-rifle-mg':             997,
  'de-inf-assault-rifle':        997,
  'br-inf-rifle-mg':             997,
  'sv-inf-rifle-mg':             997,
  'sv-spaa-dshk':                969,
  'us-transport-halftrack':      954,
  'de-transport-sdkfz251':       954,
  'br-recon-universal-carrier':  954,
  'br-recon-indian-carrier':     954,
  'br-recon-daimler-dingo':      954,
  'br-transport-white-marmon':   954,
  'br-transport-humber-scout':   954,
  'br-transport-m5-halftrack':   954,
  'us-ac-m20':                   950,
  'br-ac-m20':                   950,
};

const QUALITIES = ['Regular', 'Elite', 'Poor'];

exports.handler = async (event) => {
  const token = event.queryStringParameters && event.queryStringParameters.token;
  if (token !== process.env.KOFI_VERIFICATION_TOKEN) {
    return { statusCode: 401, body: 'Unauthorized' };
  }

  const check = event.queryStringParameters.check === 'true';

  if (check) {
    const snap = await db.ref('ratings').once('value');
    const existing = snap.val() || {};
    return {
      statusCode: 200,
      body: JSON.stringify({
        existingKeys: Object.keys(existing).length,
        seedKeys: Object.keys(SEEDED).length * QUALITIES.length,
        sample: Object.entries(existing).slice(0, 5)
      }, null, 2)
    };
  }

  // Build all rating entries
  const writes = {};
  for (const [teamId, rating] of Object.entries(SEEDED)) {
    for (const quality of QUALITIES) {
      const key = `${teamId}_${quality}`;
      writes[key] = { rating, wins: 0, losses: 0, comparisons: 0, seeded: true };
    }
  }

  // Write all in parallel
  await Promise.all(
    Object.entries(writes).map(([key, val]) =>
      db.ref(`ratings/${key}`).set(val)
    )
  );

  return {
    statusCode: 200,
    body: JSON.stringify({ seeded: Object.keys(writes).length, teams: Object.keys(SEEDED).length })
  };
};
