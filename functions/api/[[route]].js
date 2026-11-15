// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
import bundle from '../../api/dist/bundle.json' with { type: 'json' };

const datasets = new Map(bundle.regions.map((dataset) => [dataset.manifest.region.id, dataset]));
const regions = bundle.regions.map(({ manifest: { region: { id, name, bbox } } }) => ({ id, name, bbox }));

export function onRequestGet({ params: { route } }) {
  const [resource, id, file] = route;
  if (route.length === 1) {
    if (resource === 'health') return Response.json({ ok: true, version: bundle.version });
    if (resource === 'regions') return Response.json(regions);
    if (resource === 'manifest' && datasets.has('mexico_city')) {
      return Response.json(datasets.get('mexico_city').manifest);
    }
  }

  if (route.length === 3 && resource === 'regions' && (file === 'manifest' || file === 'landmarks')) {
    const dataset = datasets.get(id);
    if (dataset) return Response.json(dataset[file]);
    return Response.json({ success: false, message: 'Region not found' }, { status: 404 });
  }

  return Response.json({ success: false, message: 'Not found' }, { status: 404 });
}
