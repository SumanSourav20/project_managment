from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, Workspace, Team
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone_no = PhoneNumberField(required=False, allow_blank=True, allow_null=True)
    profile_pic = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        
        # Check if email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        
        # Check if phone number already exists (if provided)
        if data.get('phone_no') and UserProfile.objects.filter(phone_no=data['phone_no']).exists():
            raise serializers.ValidationError({"phone_no": "This phone number is already in use."})
            
        return data
    
    def create(self, validated_data):
        # Remove password_confirm from validated data
        validated_data.pop('password_confirm')
        
        # Extract profile data
        phone_no = validated_data.pop('phone_no', None)
        profile_pic = validated_data.pop('profile_pic', None)
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create profile
        profile = UserProfile.objects.create(
            user=user,
            phone_no=phone_no,
            profile_pic=profile_pic
        )
        
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_no', 'profile_pic', 'full_name']
        read_only_fields = ['id']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile
    
    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            user = instance.user
            
            for attr, value in user_data.items():
                setattr(user, attr, value)
            
            user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    users = UserProfileSerializer(many=True, read_only=True)
    workspaces = WorkspaceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at', 'users', 'workspaces']
        read_only_fields = ['id', 'created_at']


class TeamDetailSerializer(serializers.ModelSerializer):
    user_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True,
        queryset=UserProfile.objects.all(),
        source='users'
    )
    workspace_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Workspace.objects.all(),
        source='workspaces'
    )
    users = UserProfileSerializer(many=True, read_only=True)
    workspaces = WorkspaceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at', 'users', 'workspaces', 'user_ids', 'workspace_ids']
        read_only_fields = ['id', 'created_at']