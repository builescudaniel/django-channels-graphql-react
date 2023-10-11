// Importing required modules from Apollo Client library
import { ApolloClient, ApolloLink, InMemoryCache, HttpLink, split } from '@apollo/client';
import { WebSocketLink } from '@apollo/client/link/ws';
import { getMainDefinition } from '@apollo/client/utilities';

// HTTP link configuration for sending GraphQL queries and mutations via HTTP
const httpLink = new HttpLink({
    uri: 'http://localhost:8000/graphql/',
    credentials: 'include'
});

// WebSocket link configuration for GraphQL subscriptions over WebSockets
const wsLink = new WebSocketLink({
    uri: `ws://localhost:8000/graphql/`,
    options: {
        reconnect: true, // Reconnect if the connection drops
        connectionParams: {
            // Here you can include additional connection parameters if needed
            // e.g., authentication tokens
            // authToken: userToken
        }
    }
});

// ApolloLink to get the CSRF token from cookies and set it in the header for each request
const authLink = new ApolloLink((operation, forward) => {
    const csrfToken = document.cookie.split(';').find(n => n.trim().startsWith('csrftoken=')).split('=')[1];
    operation.setContext({
        headers: {
            'X-CSRFToken': csrfToken // Set CSRF token in request headers
        }
    });
    return forward(operation); // Pass the operation forward
});

// Use the split function to determine which link (http or ws) to use based on the type of GraphQL operation
const link = split(
    ({ query }) => {
        const { kind, operation } = getMainDefinition(query);
        // Return true if this is a subscription operation
        return kind === 'OperationDefinition' && operation === 'subscription';
    },
    wsLink, // Use the WebSocket link for subscriptions
    authLink.concat(httpLink) // Use the HTTP link for queries and mutations, but after setting the auth header
);

// Instantiate the ApolloClient
const client = new ApolloClient({
    cache: new InMemoryCache(), // In-memory cache to store query results
    link: link // Link to direct operations
});

// Export the configured client
export default client;