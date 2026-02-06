// frontend/src/lib/domainCheck.ts

/**
 * Checks if the current domain is in the allowlist.
 *
 * @param currentDomain The domain of the current request (e.g., 'localhost:3000', 'your-production-domain.com').
 * @param allowedDomains A comma-separated string of allowed domains from environment variables.
 * @returns true if the current domain is allowed, false otherwise.
 */
export const isDomainAllowed = (currentDomain: string, allowedDomainsEnv: string | undefined): boolean => {
    if (!allowedDomainsEnv) {
        // If no allowlist is configured, assume all domains are allowed (e.g., during development)
        return true;
    }

    const allowedDomains = allowedDomainsEnv.split(',').map(d => d.trim()).filter(d => d !== '');

    if (allowedDomains.length === 0) {
        // If allowlist is explicitly empty, allow nothing
        return false;
    }
    
    return allowedDomains.includes(currentDomain);
};
