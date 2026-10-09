# --------------------------------
#                                 #
#     Import Grype Database       #
#                                 #
# --------------------------------

# Inputs :
# GRYPE_BASE_ENDPOINT= # ! must not end with trailing '/'

# --------------------------------
# GUARD : check inputs
# --------------------------------

has_error=0

# Check GRYPE_BASE_ENDPOINT
if [ -n "${GRYPE_BASE_ENDPOINT:-}" ]; then
  echo "GRYPE_BASE_ENDPOINT is okay: $GRYPE_BASE_ENDPOINT"
else
  echo "Error: GRYPE_BASE_ENDPOINT is missing or empty." >&2
  has_error=1
fi

# Check if grype binary exists on PATH
if command -v grype >/dev/null 2>&1; then
  echo "grype binary is okay: $(command -v grype)"
else
  echo "Error: grype is missing from PATH." >&2
  has_error=1
fi

# Gate check: exit 1 if any failure occurred
if [ "$has_error" -eq 1 ]; then
  echo "Initialization gate failed." >&2
  exit 1
fi

# --------------------------------
# Script
# --------------------------------

# Fetch the official listing JSON
LISTING_JSON=$(grype db list -o json)

# Extract Database object :  status,schemaVersion,built,path,checksum
DATABASE_OBJECT=$(echo "$LISTING_JSON" | jq -r 'map(select(.schemaVersion | startswith("v6"))) | max_by(.built)')

echo $DATABASE_OBJECT

# Extract checksum and strip the "sha256:" prefix for comparison
EXPECTED_SHA=$(echo $DATABASE_OBJECT | jq -r '.checksum' | sed 's/sha256://')
# Extract file path
DB_FILE=$(echo $DATABASE_OBJECT | jq -r '.path' )


# Build URL
DB_URL=${GRYPE_BASE_ENDPOINT}/${DB_FILE}

# Download file
echo "Downloading DB from $DB_URL..."
curl -sSL "$DB_URL" -o db.tar.zst

# Calculate actual SHA256
ACTUAL_SHA=$(sha256sum db.tar.zst | awk '{print $1}')

# Verify SHA256 match
if [ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]; then
  echo "::error::Checksum mismatch! Expected $EXPECTED_SHA but got $ACTUAL_SHA"
  exit 1
fi
echo "Checksum verified successfully."

# Import the validated archive
echo "Importing vulnerability downloaded"
grype db import db.tar.zst

# Clean up the downloaded archive
echo "Cleaning up file"
rm db.tar.zst


# Display status
grype db status
