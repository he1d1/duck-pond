<script lang="ts">
  import { Map, Geocoder, Marker, controls } from "@beyonk/svelte-mapbox";
  import { onMount } from "svelte";

  const { GeolocateControl, NavigationControl, ScaleControl } = controls;

  let mapComponent;
  onMount(() =>
    mapComponent.flyTo({ center: [-1.8972671999999875, 52.481229569377945] })
  );
  // Define this to handle `eventname` events - see [GeoLocate Events](https://docs.mapbox.com/mapbox-gl-js/api/markers/#geolocatecontrol-events)
  function eventHandler(e) {
    const data = e.detail;
    // do something with `data`, it's the result returned from the mapbox event
  }
</script>

<main class="h-screen flex">
  <aside
    class="h-screen md:w-2/3 lg:w-1/2 xl:w-1/3 w-full bg-gray-200 p-4 flex flex-col gap-4"
  >
    <nav class="-m-4 mb-0 p-4 bg-gray-100 shadow flex justify-between">
      <p>Duck Pond</p>
      <p>🦆</p>
    </nav>
    <article
      class="bg-gray-100 rounded-lg w-full shadow p-4 flex items-center gap-4 divide-x divide-gray-300"
    >
      <article class="flex flex-col items-center text-yellow-500 font-bold">
        420
        <small class="font-normal">quacks</small>
      </article>
      <article class="pl-4">
        <h1 class="text-xl font-bold">Hanely Swan Duck Pond</h1>
        <small class="text-gray-600">0.4 miles · 6 min walk</small>
      </article>
    </article>
  </aside>

  <div class="map flex-1">
    <Map
      accessToken={import.meta.env.VITE_KEY}
      bind:this={mapComponent}
      on:recentre={(e) => console.log(e.detail.center.lat, e.detail.center.lng)}
      options={{ scrollZoom: false }}
    >
      <Marker
        lat={52}
        lng={-1.8}
        color="rgb(255,255,255)"
        label="Mill Pond11"
        popupClassName="class-name"
      />
      <NavigationControl />
      <GeolocateControl
        options={{ some: "control-option" }}
        on:eventname={eventHandler}
      />
      <ScaleControl />
    </Map>
  </div>
</main>

<style>
  #map {
    height: 600px;
    width: auto;
    background: #75cff0;
  }
</style>
