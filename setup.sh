git clone https://github.com/divviup/janus.git &&

cd janus &&

cargo build -r &&

docker buildx bake --load &&

cd ../ && mkdir  bin && cp janus/target/release/janus_cli ./bin && cp janus/target/release/collect ./bin && cp janus/target/release/hpke_keygen ./bin &&

# run hpke_keygen to generate a keypair for the collector
./bin/hpke_keygen 1 > collector_keypair &&

# run hpke_keygen to generate a keypair for the helper
./bin/hpke_keygen 2 > helper_keypair &&

# run hpke_keygen to generate a keypair for the leader
./bin/hpke_keygen 3 > leader_keypair &&

echo "Finished building Janus binaries and generating keypairs"
echo "Please copy the keypairs to the appropriate config files"