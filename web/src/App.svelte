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

  let selection = null;
  let selectionEntry = null;

  let state = "LIST";

  let lastClick = null;

  let name, imageURL, lat, long;
</script>

<main class="h-screen flex text-gray-900">
  <button
    on:click={() => (state = state === "MAP" ? "LIST" : "MAP")}
    class="absolute top-1/2 left-0 z-10 rounded-r-xl bg-gray-100 border-2 aspect-square w-8 h-24 transition-transform -translate-y-1/2"
    ><span>{state === "MAP" ? `>` : `<`}</span></button
  >
  {#if state !== "MAP"}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <aside
      on:click={() => (selection = null)}
      class={`h-screen md:w-2/3 lg:w-1/2 xl:w-1/3 w-full bg-gray-200 p-4 flex flex-col gap-4 overflow-y-auto ${
        selection !== null ? "hidden lg:flex" : ""
      }`}
    >
      <nav class="-m-4 mb-0 p-4 bg-gray-100 shadow flex justify-between">
        <p>Duck Pond</p>
        <p>🦆</p>
      </nav>

      <button
        on:click={() => {
          state = state === "CREATE" ? "LIST" : "CREATE";
          lastClick = null;
        }}
        class={`absolute bottom-4 left-4 rounded-full bg-gray-100 border-2 aspect-square w-12 h-12 transition-transform ${
          state === "CREATE" ? "" : "-rotate-45"
        }`}>✕</button
      >
      {#if state === "LIST"}
        {#each entries as entry, i}
          <article
            on:click|stopPropagation={() => (selection = i)}
            class={`bg-gray-100 rounded-lg w-full shadow p-4 flex items-center justify-between gap-4 ${
              selection === i ? "border-yellow-600" : ""
            }`}
          >
            <article>
              <h1 class="text-xl font-bold">
                {entry.name}
              </h1>
              <small class="text-gray-500"
                >{entry.location.lat} {entry.location.long}</small
              >
            </article>
            <article
              class="flex flex-col items-center text-yellow-600 font-bold"
            >
              {entry.votes}
              <small class="font-normal">quacks</small>
            </article>
          </article>
        {/each}
      {:else if state === "CREATE"}
        <input type="text" name="name" bind:value={name} />
        <input type="text" name="imageUrl" bind:value={imageURL} />
        <input type="number" name="latitude" bind:value={lat} />
        <input type="number" name="longitude" bind:value={long} />
        <input
          type="submit"
          on:click={async () => {
            state = "LIST";
            const body = {
              id: crypto.randomUUID(),
              name,
              imageURL,
              location: {
                lat,
                long,
              },
              votes: 0,
            };
            await fetch("http://localhost:8080/entry", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(body),
            });
            entries = [...entries, body];
          }}
        />
      {:else if state === "MAP"}{/if}
    </aside>
  {/if}
  <div class="map flex-1 relative w-full">
    {#if selection !== null}
      <article
        class="z-10 absolute inset-0 m-4 bg-gray-100 rounded-xl shadow border-2 overflow-hidden"
      >
        <button
          on:click={() => (selection = null)}
          class="absolute top-4 right-4 rounded-full bg-gray-100 border-2 aspect-square w-12 h-12"
          >✕</button
        >

        <div class="p-4">
          <small>Click to edit</small>
          <h1
            class="text-4xl font-bold"
            contenteditable="true"
            on:blur={async (event) => {
              entries[selection].name = event.target.innerHTML.split("<br>");
              console.log(entries[selection]);
              console.log(selection);
              await fetch(
                "http://localhost:8080/entry/800d2642-3962-459b-b2a5-86a39a3ee476",
                {
                  method: "PUT",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify(entries[selection]),
                }
              );
            }}
          >
            {entries[selection].name}
          </h1>

          <small class="text-gray-500"
            >{entries?.[selection].location.lat}
            {entries?.[selection].location.long}</small
          ><br />
          <button
            class="py-3 px-4 rounded-full border-2"
            on:click={async () => {
              entries[selection].votes++;
              console.log(entries[selection]);
              console.log(selection);
              await fetch(
                `http://localhost:8080/entry/${entries[selection].id}`,
                {
                  method: "PUT",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify(entries?.[selection]),
                }
              );
            }}>Quack!</button
          >
          {entries?.[selection].votes} so far
          <br />
        </div>
      </article>
    {/if}
    <Map
      accessToken={import.meta.env.VITE_KEY}
      bind:this={mapComponent}
      on:click={({ layerX: x, layerY: y }) => {
        lastClick = [x, y];
      }}
      options={{ scrollZoom: true }}
    >
      {#each entries as { name, location: { lat, long } }, i}
        <Marker
          {lat}
          lng={long}
          color="rgb(255,255,255)"
          label={`${name} (${lat} ${long})`}
          popupClassName="class-name"
        >
          <button
            class="bg-gray-100 px-3 py-2 rounded-full border-2"
            on:click={() => {
              selection = i;
              state = "LIST";
              mapComponent.flyTo({ center: [long, lat] });
            }}
          >
            {name}
          </button>
        </Marker>
      {/each}
      <NavigationControl />
      <GeolocateControl on:click={eventHandler} />
      <ScaleControl />
    </Map>
  </div>
</main>
