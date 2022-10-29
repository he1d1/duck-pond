<script lang="ts">
  import { Map, Geocoder, Marker, controls } from "@beyonk/svelte-mapbox";
  import { onMount } from "svelte";

  const { GeolocateControl, NavigationControl, ScaleControl } = controls;

  let mapComponent;
  onMount(async () => {
    mapComponent.flyTo({ center: [-1.8972671999999875, 52.481229569377945] });
    entries = await fetch("http://localhost:8080/entries", {}).then((res) =>
      res.json()
    );
  });
  // Define this to handle `eventname` events - see [GeoLocate Events](https://docs.mapbox.com/mapbox-gl-js/api/markers/#geolocatecontrol-events)
  function eventHandler(e) {
    const data = e.detail;
    // do something with `data`, it's the result returned from the mapbox event
    console.log(data);
  }
  let entries: any = [];

  $: console.log(entries);
</script>

<main class="h-screen flex">
  <aside
    class="h-screen md:w-2/3 lg:w-1/2 xl:w-1/3 w-full bg-gray-200 p-4 flex flex-col gap-4"
  >
    <nav class="-m-4 mb-0 p-4 bg-gray-100 shadow flex justify-between">
      <p>Duck Pond</p>
      <p>🦆</p>
    </nav>
    {#each entries as entry}
      <article
        class="bg-gray-100 rounded-lg w-full shadow p-4 flex items-center gap-4 divide-x divide-gray-300"
      >
        <article class="flex flex-col items-center text-yellow-500 font-bold">
          {entry.votes}
          <small class="font-normal">quacks</small>
        </article>
        <article class="pl-4">
          <h1 class="text-xl font-bold">{entry.name}</h1>
        </article>
      </article>
    {/each}
  </aside>

  <div class="map flex-1">
    <Map
      accessToken={import.meta.env.VITE_KEY}
      bind:this={mapComponent}
      on:recentre={(e) => console.log(e.detail.center.lat, e.detail.center.lng)}
      options={{ scrollZoom: false }}
    >
      {#each entries as { name, location: { lat, long } }}
        <Marker
          {lat}
          lng={long}
          color="rgb(255,255,255)"
          label={`${name} (${lat} ${long})`}
          popupClassName="class-name"
        />
      {/each}
      <NavigationControl />
      <GeolocateControl
        options={{ some: "control-option" }}
        on:eventname={eventHandler}
      />
      <ScaleControl />
    </Map>
  </div>
</main>
