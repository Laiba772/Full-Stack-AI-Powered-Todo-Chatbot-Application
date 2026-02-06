# Research Notes: ChatKit Frontend & Secure Deployment

## T001: Research best practices for integrating OpenAI ChatKit UI components with Next.js/React.

### Key Findings:
-   **OpenAI ChatKit**: Provides React components for building chat UIs. It abstracts away much of the WebSocket/polling complexity for real-time messaging.
-   **Integration**: Typically involves wrapping the application or a specific chat page with `ChatProvider` and then using components like `MessageList`, `MessageInput`.
-   **State Management**: ChatKit manages its internal UI state. For external data (like historical messages from a backend), it expects data to be passed in a specific format or through custom adapters.
-   **Customization**: Components are often customizable via props for styling and behavior.
-   **No AI/Business Logic**: Emphasized that ChatKit UI components should strictly be for rendering and input, with no AI or core business logic residing there. All message processing and AI interactions must occur through the backend.

## T002: Research secure methods for managing and attaching JWT tokens in Next.js/React applications for backend API calls.

### Key Findings:
-   **Storage Options**:
    *   **HTTP-Only Cookies**: Most secure option for storing JWTs. Prevents client-side JavaScript access, mitigating XSS attacks. Requires backend to set cookies with `HttpOnly` and `Secure` flags.
    *   **Local Storage/Session Storage**: Vulnerable to XSS. Not recommended for storing JWTs directly. Can be used for temporary, non-sensitive data.
    *   **Memory (in-app state)**: Least persistent. JWT lost on page refresh. Suitable for short-lived tokens or after retrieval from a more secure storage.
-   **Attachment to Requests**:
    *   Typically attached in the `Authorization` header as `Bearer <token>`.
    *   `axios` interceptors or custom fetch wrappers are ideal for automatically attaching tokens to all outgoing requests.
-   **Refreshing Tokens**: For long-lived sessions, a refresh token mechanism is essential. The refresh token should also be stored securely (HTTP-only cookie). When an access token expires, the client uses the refresh token to obtain a new access token without re-authenticating the user.
-   **CSRF Protection**: When using cookies, CSRF tokens should be implemented to protect against CSRF attacks.

### Recommended Strategy:
-   Store JWT (access token) in an HTTP-only, secure cookie.
-   Implement an Axios interceptor (or similar) to attach the JWT from the cookie to outgoing requests.
-   Implement a refresh token mechanism if long-lived sessions are desired, also using HTTP-only cookies for the refresh token.
