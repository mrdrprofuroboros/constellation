<script>
  import ApolloClient from "apollo-boost";
  import { setClient } from "svelte-apollo";
  import { getClient, query, mutate } from "svelte-apollo";
  import { gql } from "apollo-boost";

  import Graph from './Graph.svelte';
  import data from '../../data/sample.js'
  
  export let name = 'GraphQL';
  
  const client = new ApolloClient({
    uri: "http://localhost:4000/graphql",

    onError: ({ networkError, graphQLErrors }) => {
      console.log("graphQLErrors", graphQLErrors);
      console.log("networkError", networkError);
    }
  });

  setClient(client);

  // -------------------

  const GET_CHARLES = gql`
    {
      customer(email: "charles@gmail.com") {
        name, email
      }
    }
  `;
  const charlesOp = query(client, { query: GET_CHARLES });
</script>


<div>
	<h1 class="hello">Hello
    {#await $charlesOp}
      ..loading
    {:then result}
      {result.data.customer.name}
    {:catch e}
      {e}
    {/await}
  </h1>
	<div class="chart">
    <Graph graph={data}/>
  </div>
</div>


<style>
  :global(body) {
    margin: 0;
    background: black;
  }

  .hello {
    color: white;
  }

	.chart {
		width: 100%;
		max-width: 1500px;
		height: 1000px;
		min-height: 500px;
		max-height: 1500px;
		margin: 0 auto;
  }
</style>
