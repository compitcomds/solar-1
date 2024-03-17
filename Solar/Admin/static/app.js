const app = Vue.createApp({
    data() {
        return {
            property: [],
            errorMessage: '',
            sub_id: null, // Initialize sub_id here
            get_data:[]
        };
    },
    mounted() {
        // Fetch sub_id from a data attribute
        this.sub_id = document.getElementById('app').getAttribute('data-sub-id');
        this.get_data = document.getElementById('app').getAttribute('data-get_data');
        var validJSONData = this.get_data.replace(/'/g, '"').replace(/False/g, 'false');
        var parsedData = JSON.parse(validJSONData);
        this.get_data=parsedData
        console.log(this.get_data)
        this.property=this.get_data
        this.getcomparedata();
    },
    methods: {
        toggleEditMode(item) {
            item.editMode = !item.editMode;
        },
        addItem() {
            this.property.push({ name: '', editMode: true }); // Adding new item with edit mode enabled
        },
        removeItem(index) {
            this.property.splice(index, 1);
        },
        saveChanges(item) {
            item.editMode = false; // Exit edit mode after saving changes
        },
        goBack() {
            window.history.back();
        },
        async save() {
            try {
                if (this.property.length === 0) {
                    this.errorMessage = 'Cannot save an empty list.';
                    return;
                }
                
                // Set editMode to false for all items before sending data to the server
                const dataToSend = this.property.map(item => ({ ...item, editMode: false }));
                
                const response = await axios.post(`addcompare`, {
                    property: dataToSend,
                    sub_id:this.sub_id
                    // Sending the property data
                });
                console.log('Items added successfully:', response.data);
                // Handle response if needed
            } catch (error) {
                console.error('Error adding items:', error);
                this.errorMessage = 'Error adding items: ' + error.message; // Update error message
            }
        },
    }
});

app.mount('#app');
