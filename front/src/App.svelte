<script>
  import ApolloClient from "apollo-boost";
  import { setClient } from "svelte-apollo";

  import Graph from './Graph.svelte';
  
  export let name = 'GraphQL';
  
  const client = new ApolloClient({
    uri: "http://localhost:4000/graphql",

    onError: ({ networkError, graphQLErrors }) => {
      console.log("graphQLErrors", graphQLErrors);
      console.log("networkError", networkError);
    }
  });

  setClient(client);
</script>


<template lang="pug">
	h1 Hello {name}
	div.chart
		Graph
</template>


<style lang="stylus">
	.chart
		width: 100%
		max-width: 1500px
		height: calc(100% - 4em)
		min-height: 500px
		max-height: 1000px
		margin: 0 auto
</style>
