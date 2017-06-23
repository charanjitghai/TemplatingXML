cd /scratch/cghai/commandToCustMapping/AllCRMStandardObjectTests/AllCustomAttributeTests/MDS
all_objects=`ls`
echo $all_objects


obj_twelve=()

for object in $all_objects
do
	num_files=`find $object/ -type f | wc -l`
	if [ $num_files -ne 12 ]; then
		echo $object $num_files
	else
		obj_twelve+=($object)
	fi
done

echo "12 file objects"
for object in ${obj_twelve[@]}
do
	echo $object
	mv $object /scratch/cghai/commandToCustMapping/AllCRMStandardObjectTests/AllCustomAttributeTests/ActiveMDS
done
echo ${#obj_twelve[@]}
