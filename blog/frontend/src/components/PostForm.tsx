import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { usePosts, Post } from '@/hooks/usePosts';
import { ArrowLeft, Save, FileText, User, Type, AlignLeft } from 'lucide-react';

interface PostFormProps {
  post?: Post | null;
  onClose: () => void;
  onSuccess: () => void;
}

export const PostForm: React.FC<PostFormProps> = ({ post, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    title: '',
    description: '',
  });
  const { createPost, updatePost, loading } = usePosts();
  const isEditing = Boolean(post);

  useEffect(() => {
    if (post) {
      setFormData({
        name: post.name,
        title: post.title,
        description: post.description,
      });
    }
  }, [post]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name.trim() || !formData.title.trim() || !formData.description.trim()) {
      return;
    }

    const success = isEditing && post
      ? await updatePost(post.id, formData)
      : await createPost(formData);

    if (success) {
      onSuccess();
    }
  };

  const handleInputChange = (field: string) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData(prev => ({
      ...prev,
      [field]: e.target.value,
    }));
  };

  return (
    <div className="min-h-screen bg-secondary-gradient">
      {/* Header */}
      <header className="border-b border-border bg-card/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button
              onClick={onClose}
              variant="outline"
              size="sm"
              className="flex items-center space-x-2 hover:bg-muted transition-smooth"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Dashboard</span>
            </Button>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-gradient rounded-xl flex items-center justify-center">
                <FileText className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  {isEditing ? 'Edit Post' : 'Create New Post'}
                </h1>
                <p className="text-sm text-muted-foreground">
                  {isEditing ? 'Update your blog post' : 'Write amazing content for your readers'}
                </p>
              </div>
            </div>
          </div>
          
          <Button
            type="submit"
            form="post-form"
            disabled={loading || !formData.name.trim() || !formData.title.trim() || !formData.description.trim()}
            className="bg-primary-gradient hover:opacity-90 transition-smooth font-semibold shadow-elegant"
          >
            <Save className="w-4 h-4 mr-2" />
            {loading ? 'Saving...' : isEditing ? 'Update Post' : 'Publish Post'}
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-card/80 backdrop-blur-sm border-border shadow-elegant">
            <CardHeader className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-accent-gradient rounded-xl flex items-center justify-center">
                  <FileText className="w-6 h-6 text-foreground" />
                </div>
                <div>
                  <CardTitle className="text-2xl text-foreground">
                    {isEditing ? 'Edit Your Post' : 'Create New Post'}
                  </CardTitle>
                  <CardDescription className="text-muted-foreground">
                    {isEditing 
                      ? 'Make changes to your existing blog post'
                      : 'Fill in the details to create your new blog post'
                    }
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            
            <CardContent>
              <form id="post-form" onSubmit={handleSubmit} className="space-y-8">
                <div className="space-y-2">
                  <Label htmlFor="name" className="text-foreground font-semibold flex items-center space-x-2">
                    <User className="w-4 h-4 text-primary" />
                    <span>Author Name</span>
                  </Label>
                  <Input
                    id="name"
                    type="text"
                    placeholder="Enter author name"
                    value={formData.name}
                    onChange={handleInputChange('name')}
                    className="h-12 border-border bg-background/50 backdrop-blur-sm transition-smooth focus:shadow-soft"
                    required
                  />
                  <p className="text-xs text-muted-foreground">
                    The name that will appear as the author of this post
                  </p>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="title" className="text-foreground font-semibold flex items-center space-x-2">
                    <Type className="w-4 h-4 text-primary" />
                    <span>Post Title</span>
                  </Label>
                  <Input
                    id="title"
                    type="text"
                    placeholder="Enter an engaging title for your post"
                    value={formData.title}
                    onChange={handleInputChange('title')}
                    className="h-12 border-border bg-background/50 backdrop-blur-sm transition-smooth focus:shadow-soft text-lg"
                    required
                  />
                  <p className="text-xs text-muted-foreground">
                    A compelling title that captures your readers' attention
                  </p>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="description" className="text-foreground font-semibold flex items-center space-x-2">
                    <AlignLeft className="w-4 h-4 text-primary" />
                    <span>Post Content</span>
                  </Label>
                  <Textarea
                    id="description"
                    placeholder="Write your blog post content here... Share your thoughts, stories, and insights with your readers."
                    value={formData.description}
                    onChange={handleInputChange('description')}
                    className="min-h-96 resize-none border-border bg-background/50 backdrop-blur-sm transition-smooth focus:shadow-soft text-base leading-relaxed"
                    required
                  />
                  <p className="text-xs text-muted-foreground">
                    The main content of your blog post. Write as much as you want to engage your readers.
                  </p>
                </div>

                {/* Preview Section */}
                <div className="border-t border-border pt-8">
                  <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center space-x-2">
                    <FileText className="w-5 h-5 text-primary" />
                    <span>Preview</span>
                  </h3>
                  <Card className="bg-accent-gradient border-border">
                    <CardHeader>
                      <CardTitle className="text-xl text-foreground">
                        {formData.title || 'Your post title will appear here'}
                      </CardTitle>
                      <CardDescription className="text-muted-foreground">
                        By {formData.name || 'Author name'}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <p className="text-foreground leading-relaxed">
                        {formData.description || 'Your post content will appear here as you type...'}
                      </p>
                    </CardContent>
                  </Card>
                </div>

                <div className="flex items-center justify-end space-x-4 pt-6 border-t border-border">
                  <Button
                    type="button"
                    onClick={onClose}
                    variant="outline"
                    className="hover:bg-muted transition-smooth"
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    disabled={loading || !formData.name.trim() || !formData.title.trim() || !formData.description.trim()}
                    className="bg-primary-gradient hover:opacity-90 transition-smooth font-semibold shadow-elegant px-8"
                  >
                    <Save className="w-4 h-4 mr-2" />
                    {loading ? 'Saving...' : isEditing ? 'Update Post' : 'Publish Post'}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};