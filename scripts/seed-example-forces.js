/**
 * Seed Example Forces — Hail of Fire Arsenal
 *
 * SETUP:
 * 1. Download a Firebase service account key from:
 *    Firebase Console → Project Settings → Service Accounts → Generate new private key
 *    Save it as serviceAccount.json in the repo root (it's gitignored).
 *
 * 2. Run from the repo root:
 *    NODE_PATH="netlify/functions/node_modules" node scripts/seed-example-forces.js
 *
 * Or with the env var instead of a file:
 *    FIREBASE_SERVICE_ACCOUNT="$(cat serviceAccount.json)" NODE_PATH="netlify/functions/node_modules" node scripts/seed-example-forces.js
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

if (!admin.apps.length) {
  let serviceAccount;
  if (process.env.FIREBASE_SERVICE_ACCOUNT) {
    serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);
  } else {
    const saPath = path.join(__dirname, '..', 'serviceAccount.json');
    if (!fs.existsSync(saPath)) {
      console.error('ERROR: No credentials found.');
      console.error('Download a service account key from Firebase Console and save as serviceAccount.json in the repo root.');
      process.exit(1);
    }
    serviceAccount = JSON.parse(fs.readFileSync(saPath, 'utf8'));
  }
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: 'https://hailoffire-campaign-default-rtdb.firebaseio.com'
  });
}

const db = admin.database();

// ── FORCE DEFINITIONS ─────────────────────────────────────────────────────────
// Based on the Example Forces in the Hail of Fire rulebook (p. 14)

const forces = [

  // ── UNITED STATES ────────────────────────────────────────────────────────────

  {
    name: 'US Rifle Company (1944–45)',
    notes: 'Standard US infantry company as organized in NW Europe and Italy. Three rifle platoons supported by organic anti-tank, tank, mortar, and artillery assets. Versatile and well-supported.',
    author: 'Hail of Fire',
    authorUid: null,
    nations: ['United States'],
    published: true,
    platoons: [
      {
        name: '1st Rifle Platoon',
        teams: [
          { unitId: 'us-leader', qty: 1 },
          { unitId: 'us-inf-bazooka', qty: 1 },
          { unitId: 'us-inf-rifle-mg', qty: 6 },
        ]
      },
      {
        name: '2nd Rifle Platoon',
        teams: [
          { unitId: 'us-leader', qty: 1 },
          { unitId: 'us-inf-bazooka', qty: 1 },
          { unitId: 'us-inf-rifle-mg', qty: 6 },
        ]
      },
      {
        name: '3rd Rifle Platoon',
        teams: [
          { unitId: 'us-leader', qty: 1 },
          { unitId: 'us-inf-bazooka', qty: 1 },
          { unitId: 'us-inf-rifle-mg', qty: 6 },
        ]
      },
      {
        name: 'Anti-Tank Platoon',
        teams: [
          { unitId: 'us-leader', qty: 1 },
          { unitId: 'us-gun-57mm', qty: 3 },
        ]
      },
      {
        name: 'Tank Platoon',
        teams: [
          { unitId: 'us-tank-m4-sherman', qty: 3 },
        ]
      },
      {
        name: 'Mortar Platoon',
        teams: [
          { unitId: 'us-leader', qty: 1 },
          { unitId: 'us-fo', qty: 1 },
          { unitId: 'us-gun-81mm-mortar', qty: 3 },
        ]
      },
      {
        name: 'Artillery Battery',
        teams: [
          { unitId: 'us-leader', qty: 1 },
          { unitId: 'us-fo', qty: 1 },
          { unitId: 'us-gun-155mm-howitzer', qty: 3 },
        ]
      },
    ]
  },

  {
    name: 'US Tank Company (1944–45)',
    notes: 'Combined arms tank company from NW Europe. Two tank platoons with an armored rifle platoon riding halftracks, a Stuart recon element, and M7 Priest artillery support.',
    author: 'Hail of Fire',
    authorUid: null,
    nations: ['United States'],
    published: true,
    platoons: [
      {
        name: '1st Tank Platoon',
        teams: [
          { unitId: 'us-tank-m4-sherman', qty: 3 },
        ]
      },
      {
        name: '2nd Tank Platoon',
        teams: [
          { unitId: 'us-tank-m4-sherman', qty: 3 },
        ]
      },
      {
        name: 'Armored Rifle Platoon',
        teams: [
          { unitId: 'us-leader', qty: 1 },
          { unitId: 'us-inf-bazooka', qty: 2 },
          { unitId: 'us-gun-60mm-mortar', qty: 1 },
          { unitId: 'us-inf-mg', qty: 6 },
          { unitId: 'us-transport-halftrack', qty: 4 },
        ]
      },
      {
        name: 'Recon Platoon',
        teams: [
          { unitId: 'us-tank-m5-stuart', qty: 3 },
        ]
      },
      {
        name: 'Artillery Battery',
        teams: [
          { unitId: 'us-fo', qty: 1 },
          { unitId: 'us-spa-m7-priest', qty: 3 },
        ]
      },
    ]
  },

  // ── GERMANY ───────────────────────────────────────────────────────────────────

  {
    name: 'German Grenadier Company (1944–45)',
    notes: 'Late-war German infantry company. Grenadier platoons are armed with Panzerfausts giving them a real anti-tank capability. Supported by PaK40 anti-tank guns, StuG assault guns, mortars, and the fearsome 88mm FlaK.',
    author: 'Hail of Fire',
    authorUid: null,
    nations: ['Germany'],
    published: true,
    platoons: [
      {
        name: '1st Grenadier Platoon',
        teams: [
          { unitId: 'de-leader', qty: 1 },
          { unitId: 'de-inf-rifle-mg', qty: 6 },
          { unitId: 'de-inf-panzerfaust', qty: 2 },
        ]
      },
      {
        name: '2nd Grenadier Platoon',
        teams: [
          { unitId: 'de-leader', qty: 1 },
          { unitId: 'de-inf-rifle-mg', qty: 6 },
          { unitId: 'de-inf-panzerfaust', qty: 2 },
        ]
      },
      {
        name: '3rd Grenadier Platoon',
        teams: [
          { unitId: 'de-leader', qty: 1 },
          { unitId: 'de-inf-rifle-mg', qty: 6 },
          { unitId: 'de-inf-panzerfaust', qty: 2 },
        ]
      },
      {
        name: 'Anti-Tank Platoon',
        teams: [
          { unitId: 'de-leader', qty: 1 },
          { unitId: 'de-gun-pak40', qty: 2 },
        ]
      },
      {
        name: 'Panzer Platoon',
        teams: [
          { unitId: 'de-tank-stug', qty: 3 },
        ]
      },
      {
        name: 'Mortar Platoon',
        teams: [
          { unitId: 'de-leader', qty: 1 },
          { unitId: 'de-fo', qty: 1 },
          { unitId: 'de-gun-8cm-mortar', qty: 3 },
        ]
      },
      {
        name: 'Heavy AA Platoon',
        teams: [
          { unitId: 'de-leader', qty: 1 },
          { unitId: 'de-gun-88mm-flak', qty: 1 },
        ]
      },
    ]
  },

  {
    name: 'German Panzer Company (1944–45)',
    notes: 'Late-war Panzer company built around Panzer IV platoons. Panzergrenadiers ride Sd Kfz 251 halftracks. Puma armored cars provide recon and the Wespe offers mobile artillery support.',
    author: 'Hail of Fire',
    authorUid: null,
    nations: ['Germany'],
    published: true,
    platoons: [
      {
        name: '1st Panzer Platoon',
        teams: [
          { unitId: 'de-tank-pz4h', qty: 3 },
        ]
      },
      {
        name: '2nd Panzer Platoon',
        teams: [
          { unitId: 'de-tank-pz4h', qty: 3 },
        ]
      },
      {
        name: 'Panzergrenadier Platoon',
        teams: [
          { unitId: 'de-leader', qty: 1 },
          { unitId: 'de-inf-panzerschreck', qty: 1 },
          { unitId: 'de-inf-mg', qty: 6 },
          { unitId: 'de-transport-sdkfz251', qty: 4 },
        ]
      },
      {
        name: 'Recon Platoon',
        teams: [
          { unitId: 'de-ac-puma', qty: 2 },
        ]
      },
      {
        name: 'Artillery Battery',
        teams: [
          { unitId: 'de-fo', qty: 1 },
          { unitId: 'de-spa-wespe', qty: 3 },
        ]
      },
    ]
  },

  // ── SOVIET UNION ──────────────────────────────────────────────────────────────

  {
    name: 'Soviet Strelkovy Company (1944)',
    notes: 'Soviet rifle company at the height of Soviet power. Large Strelkovy platoons include HMG and AT rifle teams as organic support. Backed by mortars, anti-tank guns, T-34s, and heavy artillery.',
    author: 'Hail of Fire',
    authorUid: null,
    nations: ['Soviet Union'],
    published: true,
    platoons: [
      {
        name: '1st Rifle Platoon',
        teams: [
          { unitId: 'sv-leader', qty: 1 },
          { unitId: 'sv-gun-maksim', qty: 1 },
          { unitId: 'sv-gun-ptrd', qty: 1 },
          { unitId: 'sv-inf-rifle-mg', qty: 6 },
        ]
      },
      {
        name: '2nd Rifle Platoon',
        teams: [
          { unitId: 'sv-leader', qty: 1 },
          { unitId: 'sv-gun-maksim', qty: 1 },
          { unitId: 'sv-gun-ptrd', qty: 1 },
          { unitId: 'sv-inf-rifle-mg', qty: 6 },
        ]
      },
      {
        name: '3rd Rifle Platoon',
        teams: [
          { unitId: 'sv-leader', qty: 1 },
          { unitId: 'sv-gun-maksim', qty: 1 },
          { unitId: 'sv-gun-ptrd', qty: 1 },
          { unitId: 'sv-inf-rifle-mg', qty: 6 },
        ]
      },
      {
        name: 'Mortar Platoon',
        teams: [
          { unitId: 'sv-leader', qty: 1 },
          { unitId: 'sv-fo', qty: 1 },
          { unitId: 'sv-gun-82mm-mortar', qty: 4 },
        ]
      },
      {
        name: 'Anti-Tank Platoon',
        teams: [
          { unitId: 'sv-leader', qty: 1 },
          { unitId: 'sv-gun-45mm', qty: 3 },
        ]
      },
      {
        name: 'Tank Platoon',
        teams: [
          { unitId: 'sv-tank-t34-85', qty: 3 },
        ]
      },
      {
        name: 'Artillery Battery',
        teams: [
          { unitId: 'sv-leader', qty: 1 },
          { unitId: 'sv-fo', qty: 1 },
          { unitId: 'sv-gun-152mm-howitzer', qty: 3 },
        ]
      },
    ]
  },

  {
    name: 'Soviet Tankovy Company (1944)',
    notes: 'Soviet armored company featuring two T-34 platoons and an SU-85 tank destroyer platoon. Motorized infantry rides ZIS trucks. BA-64 armored cars provide recon, Katyusha rockets deliver mass fire support.',
    author: 'Hail of Fire',
    authorUid: null,
    nations: ['Soviet Union'],
    published: true,
    platoons: [
      {
        name: '1st Tank Platoon',
        teams: [
          { unitId: 'sv-tank-t34-85', qty: 3 },
        ]
      },
      {
        name: '2nd Tank Platoon',
        teams: [
          { unitId: 'sv-tank-t34-85', qty: 3 },
        ]
      },
      {
        name: 'Rifle Platoon',
        teams: [
          { unitId: 'sv-leader', qty: 1 },
          { unitId: 'sv-gun-maksim', qty: 1 },
          { unitId: 'sv-gun-ptrd', qty: 1 },
          { unitId: 'sv-inf-rifle-mg', qty: 6 },
          { unitId: 'sv-transport-zis-truck', qty: 4 },
        ]
      },
      {
        name: 'SU-85 Platoon',
        teams: [
          { unitId: 'sv-spg-su85', qty: 3 },
        ]
      },
      {
        name: 'Recon Platoon',
        teams: [
          { unitId: 'sv-ac-ba64', qty: 2 },
        ]
      },
      {
        name: 'Artillery Battery',
        teams: [
          { unitId: 'sv-fo', qty: 1 },
          { unitId: 'sv-spa-katyusha', qty: 3 },
        ]
      },
    ]
  },

  // ── BRITISH & COMMONWEALTH ────────────────────────────────────────────────────

  {
    name: 'British Rifle Company (1944–45)',
    notes: 'Standard British infantry company from NW Europe. Each rifle platoon includes a PIAT and 2" mortar as organic support. Backed by 6-pounder anti-tank guns, Churchill tanks, 3" mortars, and BL 5.5" guns.',
    author: 'Hail of Fire',
    authorUid: null,
    nations: ['Britain'],
    published: true,
    platoons: [
      {
        name: '1st Rifle Platoon',
        teams: [
          { unitId: 'br-leader', qty: 1 },
          { unitId: 'br-inf-piat', qty: 1 },
          { unitId: 'br-inf-2in-mortar', qty: 1 },
          { unitId: 'br-inf-rifle-mg', qty: 6 },
        ]
      },
      {
        name: '2nd Rifle Platoon',
        teams: [
          { unitId: 'br-leader', qty: 1 },
          { unitId: 'br-inf-piat', qty: 1 },
          { unitId: 'br-inf-2in-mortar', qty: 1 },
          { unitId: 'br-inf-rifle-mg', qty: 6 },
        ]
      },
      {
        name: '3rd Rifle Platoon',
        teams: [
          { unitId: 'br-leader', qty: 1 },
          { unitId: 'br-inf-piat', qty: 1 },
          { unitId: 'br-inf-2in-mortar', qty: 1 },
          { unitId: 'br-inf-rifle-mg', qty: 6 },
        ]
      },
      {
        name: 'Anti-Tank Platoon',
        teams: [
          { unitId: 'br-leader', qty: 1 },
          { unitId: 'br-gun-6pdr', qty: 3 },
        ]
      },
      {
        name: 'Tank Platoon',
        teams: [
          { unitId: 'br-tank-churchill34', qty: 3 },
        ]
      },
      {
        name: 'Mortar Platoon',
        teams: [
          { unitId: 'br-leader', qty: 1 },
          { unitId: 'br-fo', qty: 1 },
          { unitId: 'br-gun-3in-mortar', qty: 3 },
        ]
      },
      {
        name: 'Artillery Battery',
        teams: [
          { unitId: 'br-leader', qty: 1 },
          { unitId: 'br-fo', qty: 1 },
          { unitId: 'br-gun-55in', qty: 3 },
        ]
      },
    ]
  },

  {
    name: 'British Tank Company (1944–45)',
    notes: 'British armoured squadron from NW Europe. Each tank troop pairs two Cromwells with a Sherman Firefly for long-range AT punch. Motor platoon provides infantry support. Stuart recon and Sexton SP artillery round out the force.',
    author: 'Hail of Fire',
    authorUid: null,
    nations: ['Britain'],
    published: true,
    platoons: [
      {
        name: '1st Tank Troop',
        teams: [
          { unitId: 'br-tank-cromwell4', qty: 2 },
          { unitId: 'br-tank-firefly', qty: 1 },
        ]
      },
      {
        name: '2nd Tank Troop',
        teams: [
          { unitId: 'br-tank-cromwell4', qty: 2 },
          { unitId: 'br-tank-firefly', qty: 1 },
        ]
      },
      {
        name: 'Motor Platoon',
        teams: [
          { unitId: 'br-leader', qty: 1 },
          { unitId: 'br-inf-piat', qty: 1 },
          { unitId: 'br-inf-2in-mortar', qty: 1 },
          { unitId: 'br-inf-mg', qty: 6 },
          { unitId: 'br-transport-m5-halftrack', qty: 4 },
        ]
      },
      {
        name: 'Recon Platoon',
        teams: [
          { unitId: 'br-tank-stuart', qty: 3 },
        ]
      },
      {
        name: 'Artillery Battery',
        teams: [
          { unitId: 'br-fo', qty: 1 },
          { unitId: 'br-spa-sexton', qty: 3 },
        ]
      },
    ]
  },

];

// ── SEED ──────────────────────────────────────────────────────────────────────

async function seed() {
  const now = Date.now();
  const ref = db.ref('forces');

  for (const force of forces) {
    const platoonCount = force.platoons.length;
    const breakLimit = 5 + platoonCount * 2;

    const entry = {
      name: force.name,
      notes: force.notes,
      author: force.author,
      authorUid: force.authorUid,
      authorEmail: null,
      nations: force.nations,
      platoonCount,
      breakLimit,
      platoons: force.platoons,
      created: now,
      published: force.published,
    };

    const newRef = ref.push();
    entry.id = newRef.key;
    await newRef.set(entry);
    console.log(`✓ Seeded: ${force.name} (${platoonCount} platoons, BL ${breakLimit}) — id: ${entry.id}`);
  }

  console.log('\nAll example forces seeded successfully.');
  process.exit(0);
}

seed().catch(err => {
  console.error('Seed failed:', err);
  process.exit(1);
});
