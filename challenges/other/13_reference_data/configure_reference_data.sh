# hide a flag in a .loc file

sed -i 's|</tables>|    <!-- ctf reference data --> \
    <table name="ctf_reference_data" comment_char="#" allow_duplicate_entries="False"> \
        <columns>value, name, url</columns> \
        <file path="tool-data/ctf.loc" /> \
    </table> \
</tables>|' $GALAXY_ROOT/config/tool_data_table_conf.xml.sample

echo "ctf\tdata\tgccctf{little_bobby_data_tables}" > $GALAXY_ROOT/tool-data/ctf.loc
