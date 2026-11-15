// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
import bundle from '../../api/dist/bundle.json' with { type: 'json' };

const datasets = new Map(bundle.regions.map((dataset) => [dataset.manifest.region.id, dataset]));
const regions = bundle.regions.map(({ manifest: { region: { id, name, bbox } } }) => ({ id, name, bbox }));
const notFound = (message) => Response.json({ success: false, message }, { status: 404 });

export function onRequestGet({ params }) {
  const route = params.route ?? [];
  const [resource, id, file = 'manifest'] = route;
  if (route.length === 1) {
    if (resource === 'health') return Response.json({ ok: true, version: bundle.version });
    if (resource === 'regions') return Response.json(regions);
    if (resource === 'landmarks') return regionFile('mexico_city', 'landmarks');
  }
  if (resource === 'regions' && (route.length === 2 || route.length === 3) &&
      (file === 'manifest' || file === 'landmarks')) {
    return regionFile(id, file);
  }
  return notFound('Not found');
}

function regionFile(id, file) {
  const dataset = datasets.get(id);
  return dataset ? Response.json(dataset[file]) : notFound('Region not found');
}
